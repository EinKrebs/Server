import asyncio
import os
from typing import Tuple

from request.http_request import HttpRequest
from response.http_response import HttpResponse
from response.response_code import Code


class Server:
    def __init__(self, port: int = 12345):
        self.handlers = {}
        self.host_handlers = {}
        self.port = port

    def text(self, addr, host=None):
        from server_functions.text import text
        return text(self, addr, host)

    def file(self, addr, host=None):
        from server_functions.file import file
        return file(self, addr, host)

    def directory_listing(self, addr, host=None, view=None):
        from server_functions.directory_listing import directory_listing
        if view is not None:
            return directory_listing(self, addr, host, view=view)
        else:
            return directory_listing(self, addr, host)

    def custom_handler(self, addr, host=None):
        from server_functions.custom_hadler import custom_handler
        return custom_handler(self, addr, host)

    async def start(self):
        async with await asyncio.start_server(self.handle_connection,
                                              '127.0.0.1',
                                              self.port) as server:
            print(f'Serving on http://127.0.0.1:{self.port}/')
            await server.serve_forever()

    async def handle_connection(self, reader: asyncio.StreamReader,
                                writer: asyncio.StreamWriter):
        while True:
            try:
                data = await reader.readuntil(b'\r\n\r\n')

            except asyncio.IncompleteReadError:
                break
            answer, keep = await self.handle_request(data, reader)
            writer.write(answer.to_bytes())
            await writer.drain()
            if not keep:
                break
        writer.close()
        await writer.wait_closed()

    async def handle_request(self,
                       data: bytes,
                       reader: asyncio.StreamReader) -> \
            Tuple[HttpResponse, bool]:
        req = HttpRequest.from_bytes(data)
        if 'Content-Length' in req.headers and req.form is None:
            length = int(req.headers['Content-Length'])
            data += await reader.read(length)
            print(data[-length:])
            req = HttpRequest.from_bytes(data)
        if req.address not in self.handlers:
            return HttpResponse(Code.PAGE_NOT_FOUND), False
        handler = self.handlers[req.address]
        res = handler(req)
        return res, req.headers['Connection'] == 'keep-alive'

    def bind(self, host, addr, handler):
        if host is not None:
            if host not in self.host_handlers:
                self.host_handlers[host] = {}
            if addr in self.host_handlers[host]:
                raise ValueError("handler defined already")
            self.host_handlers[host][addr] = handler
        else:
            if addr in self.handlers:
                raise ValueError("handler defined already")
            self.handlers[addr] = handler
