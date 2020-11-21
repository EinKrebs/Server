import asyncio

from request.http_request import HttpRequest
from response.http_response import HttpResponse
from response.response_code import Code


class Server:
    def __init__(self, port: int = 12345):
        self.handlers = {}
        self.port = port

    def text(self, addr):
        def decor(func):
            def result(request: HttpRequest) -> HttpResponse:
                answer_data = func(request)
                return HttpResponse(Code.OK, answer_data)
            self.handlers[addr] = result
            return result
        return decor

    def add_route(self, addr, handler):
        self.handlers[addr] = handler

    async def start(self):
        async with await asyncio.start_server(self.handle_connection, '127.0.0.1', self.port) as server:
            await server.serve_forever()

    async def handle_connection(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        while True:
            try:
                data = await reader.readuntil(b'\r\n\r\n')
            except asyncio.IncompleteReadError:
                break
            answer = self.handle_request(data)
            writer.write(answer.to_bytes())
            await writer.drain()
        writer.close()
        await writer.wait_closed()

    def handle_request(self, data: bytes) -> HttpResponse:
        req = HttpRequest.from_bytes(data)
        if req.address not in self.handlers:
            return HttpResponse(Code.PAGE_NOT_FOUND)
        handler = self.handlers[req.address]
        res = handler(req)
        return res
