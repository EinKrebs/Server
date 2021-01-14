from request.http_request import HttpRequest
from response.http_response import HttpResponse


def custom_handler(server, addr, host=None):
    def decor(func):
        def handler(request: HttpRequest) -> HttpResponse:
            return func(request)
        server._bind(host, addr, handler)
        return handler

    return decor
