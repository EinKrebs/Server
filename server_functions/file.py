from request.http_request import HttpRequest
from response.http_response import HttpResponse
from response.response_code import Code


def file(server, addr, host=None):
    def decor(func):
        def handler(request: HttpRequest) -> HttpResponse:
            filename = func(request)
            return HttpResponse(Code.OK, file=filename)

        server.bind(host, addr, handler)
        return handler

    return decor
