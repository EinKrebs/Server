import asyncio
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
        def decor(func):
            def result(request: HttpRequest) -> HttpResponse:
                answer_data = func(request)
                return HttpResponse(Code.OK, answer_data)

            self.bind(host, addr, result)
            return result

        return decor

    def file(self, addr, host=None):
        def decor(func):
            def handler(request) -> HttpResponse:
                filename = func(request)
                return HttpResponse(Code.OK, file=filename)

            self.bind(host, addr, handler)
            return handler

        return decor

    def add_route(self, addr, handler):
        self.handlers[addr] = handler

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
            answer, keep = self.handle_request(data)
            writer.write(answer.to_bytes())
            await writer.drain()
            if not keep:
                break
        writer.close()
        await writer.wait_closed()

    def handle_request(self, data: bytes) -> Tuple[HttpResponse, bool]:
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
