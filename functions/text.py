from server import Server
from request.http_request import HttpRequest
from response.http_response import HttpResponse
from response.response_code import Code


def text(server: Server, addr):
    def decor(func):
        def result(request: HttpRequest) -> HttpResponse:
            answer_data = func(request)
            return HttpResponse(Code.OK, answer_data)
        server.handlers[addr] = result
        return result
    return decor
