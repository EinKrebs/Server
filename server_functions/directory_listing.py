from request.http_request import HttpRequest
from response.http_response import HttpResponse
from response.response_code import Code
import html_functions
import os


def directory_listing(server, addr, host=None):
    def decor(func):
        def handler(request: HttpRequest) -> HttpResponse:
            directory_name = func(request)
            text = html_functions.base_structure(
                directory_name[directory_name.rfind('/') + 1:],
                html_functions.block(
                    'pre',
                    '\n'.join(file for file in os.listdir(directory_name))
                )
            )
            return HttpResponse(Code.OK, text_data=text)

        server.bind(host, addr, handler)
        return handler

    return decor


