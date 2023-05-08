#  file: aio_echo_server.py
#  project: echo_server
#  Copyright (c) 2023. Pavlov Akeksey

"""
In general, protocol implementations that use transport-based APIs such as
loop.create_connection() and loop.create_server() are faster than
implementations that work with sockets directly.
https://docs.python.org/3/library/asyncio-eventloop.html#working-with-socket-objects-directly
"""

import asyncio
import logging


BIND_PORT = 3778
BIND_ADDRESS = "0.0.0.0"
BACKLOG = 10
BUFFER = 4096
EXIT_MSG = ["/quit", "/exit"]
LOG_FORMAT = '{asctime} - {levelname}: {message}'

logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG, style="{")
logger = logging.getLogger(__name__)


async def handle_echo(reader, writer):
    while True:
        recived_msg = await reader.read(BUFFER)
        string_msg = recived_msg.decode("UTF-8").strip()
        addr, port = writer.get_extra_info('peername')
        logger.debug(f"Received {string_msg!r} from '{addr}:{port}'")

        if string_msg in EXIT_MSG:
            logger.debug(f"Close the connection with '{addr}:{port}'")
            writer.close()
            await writer.wait_closed()
            break
        else:
            logger.debug(f"Send: {string_msg!r}")
            writer.write(recived_msg)
            await writer.drain()


async def main():
    server = await asyncio.start_server(
        handle_echo, BIND_ADDRESS, BIND_PORT)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    logger.debug(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
