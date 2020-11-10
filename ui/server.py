from infrastructure.server_functions import ServerFunctions
from request.http_request import HttpRequest
from responce.http_responce import HttpResponse
from responce.response_code import Code


class Server:
    def __init__(self, port: int = 12345):
        self.handlers = {}
        self.port = port

    def text(self, addr):
        def decor(func):
            def result(request) -> HttpResponse:
                answer_data = func(request)
                return HttpResponse(Code.OK, answer_data)
            self.handlers[addr] = result
            return result
        return decor

    def add_route(self, addr, handler):
        self.handlers[addr] = handler

    async def start(self):
        await ServerFunctions.start_server(self)

    async def handle(self, data):
        req = HttpRequest.from_bytes(data)
        if req.address not in self.handlers:
            return HttpResponse(Code.PAGE_NOT_FOUND)
        handler = self.handlers[req.address]
        res = handler(req)
        return res
