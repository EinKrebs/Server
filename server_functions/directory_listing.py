from request.http_request import HttpRequest
from response.http_response import HttpResponse
from response.response_code import Code
import html_functions
import os


def default_view(file: str):
    return file


def directory_listing(server, addr, host=None, view=default_view):
    def decor(func):
        def handler(request: HttpRequest) -> HttpResponse:
            directory_name = func(request)
            text = html_functions.base_structure(
                directory_name[directory_name.rfind('/') + 1:],
                html_functions.block(
                    'pre',
                    '\n'.join(view(file) for file in os.listdir(directory_name))
                )
            )
            return HttpResponse(Code.OK, text_data=text)

        server.bind(host, addr, handler)
        return handler

    return decor


