#  file: echo_server.py
#  project: echo_server
#  Copyright (c) 2023. Pavlov Akeksey

import logging
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, SHUT_RDWR

from select import select

BIND_PORT = 3778
BIND_ADDRESS = "0.0.0.0"
BACKLOG = 10
BUFFER = 4096
LOG_FORMAT = '{asctime} - {levelname}: {message}'
READ_FD = []
EXIT_MSG = ["quit", "exit"]

logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG, style="{")
logger = logging.getLogger(__name__)


def _str_sock(sock: socket) -> str:
    addr, port = sock.getpeername()
    return f"{addr}:{port}"


def run_server(ip_addr=BIND_ADDRESS, tcp_port=BIND_PORT):
    logger.debug(f"Start Server and bind to socket {ip_addr}:{tcp_port}")
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server_socket.bind((ip_addr, tcp_port))
    server_socket.listen(BACKLOG)
    logger.debug(f"Server is started")
    return server_socket


def accept_connection(srv_socket: socket) -> None:
    client_socket, _ = srv_socket.accept()
    logger.debug(f"Accept connection from `{_str_sock(client_socket)}`")
    READ_FD.append(client_socket)


def recive_and_send_message(clnt_socket: socket):
    recived_msg = clnt_socket.recv(BUFFER)
    string_msg = recived_msg.decode('UTF-8').strip()
    logger.debug(f"Reccived message `{string_msg}` from client socket `{_str_sock(clnt_socket)}`")
    if string_msg.lower() in EXIT_MSG:
        logger.debug(f"Remove socket `{_str_sock(clnt_socket)}` from monitoring.")
        READ_FD.remove(clnt_socket)
        clnt_socket.shutdown(SHUT_RDWR)
        logger.debug(f"Client socket `{_str_sock(clnt_socket)}` is closed.")
    else:
        clnt_socket.send(recived_msg)


def event_loop(srvr_socket):
    READ_FD.append(srvr_socket)
    while True:
        logger.debug(f"{READ_FD=}")
        to_read, _, _ = select(READ_FD, [], [])  # read, write, error
        for sock in to_read:
            if sock == srvr_socket:
                accept_connection(sock)
            else:
                recive_and_send_message(sock)


if __name__ == "__main__":
    server = run_server()
    event_loop(server)
