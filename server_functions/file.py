from request.http_request import HttpRequest
from response.http_response import HttpResponse
from response.response_code import Code


def file(server, addr, host=None, const=False):
    def decor(func):
        if const:
            file_name = func(None)
        else:
            file_name = None

        def handler(request: HttpRequest) -> HttpResponse:
            nonlocal file_name
            return HttpResponse(Code.OK, file=file_name or func(request))

        server._bind(host, addr, handler)
        return handler

    return decor
