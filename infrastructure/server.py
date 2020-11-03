import sys
import socket


def start_server(address, port, handler):
    sock = socket.socket(socket.AI_DEFAULT, socket.AF_INET)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 10)
    sock.connect((address, port))
    print(f'Connected to {address}', file=sys.stderr)
    sock.listen()
    while True:
        data = sock.recv(65535)
        if not data:
            break
        await handler(data)
