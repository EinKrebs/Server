import random
import os

from request.http_request import HttpRequest
from request.request_method import Method
from response.http_response import HttpResponse
from response.response_code import Code

from html_functions import form


def custom_handler(server, addr, host=None):
    def decor(func):
        def handler(request: HttpRequest) -> HttpResponse:
            return func(request)
        server.bind(host, addr, handler)
        return handler

    return decor

