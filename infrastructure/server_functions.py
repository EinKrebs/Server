import sys
import socket
import asyncio


class ServerFunctions:
    @staticmethod
    async def start_server(server):
        with socket.socket() as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 10)
            sock.bind(('127.0.0.1', server.port))
            sock.listen()
            print(f'Started', file=sys.stderr)
            while True:
                conn, addr = sock.accept()
                await ServerFunctions.handle_connection(conn,
                                                        addr,
                                                        server)

    @staticmethod
    async def handle_connection(conn, addr, server):
        print(f'Connected to {addr}', file=sys.stderr)
        while True:
            request = ''
            data = conn.recv(65535)
            while request.find('\r\n\r\n') != -1 and data:
                request += data.decode()
                data = conn.recv(65535)
            await ServerFunctions.handle(conn, server, data)

    @staticmethod
    async def handle(sock: socket.socket, server, data: bytes):
        ans = await server.handle_request(data)
        try:
            sock.sendall(ans.to_bytes())
        except BrokenPipeError:
            sock.close()
