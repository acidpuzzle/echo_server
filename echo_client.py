#  file: echo_client.py
#  project: echo_server
#  Copyright (c) 2023. Pavlov Akeksey

from socket import socket, SHUT_RDWR


EXIT_MSG = ["/quit", "/exit"]


def client_program(host, port):
    client_socket = socket()
    client_socket.connect((host, port))

    message = input(" -> ") + "\n"

    while True:
        if message.lower().strip() in EXIT_MSG:
            client_socket.send(message.encode())
            client_socket.shutdown(SHUT_RDWR)
            break
        client_socket.send(message.encode())
        data = client_socket.recv(1024).decode("UTF-8")

        print('Received from server: ' + data)

        message = input(" -> ") + "\n"

    client_socket.close()


if __name__ == '__main__':
    client_program("localhost", 3778)
