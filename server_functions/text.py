from request.http_request import HttpRequest
from response.http_response import HttpResponse
from response.response_code import Code


def text(server, addr, host=None):
    def decor(func):
        def handler(request: HttpRequest) -> HttpResponse:
            answer_data = func(request)
            return HttpResponse(Code.OK, answer_data)

        server.bind(host, addr, handler)
        return handler

    return decor
