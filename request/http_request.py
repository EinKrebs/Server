from __future__ import annotations
import typing

from infrastructure.iterator_extensions import (to_dictionary)
from request.request_method import Method


class HttpRequest:
    def __init__(self, method: Method,
                 address: str,
                 params: typing.Dict[str, str] = None,
                 headers: typing.Dict[str, str] = None,
                 cookies: typing.Dict[str, str] = None,
                 valid: bool = True):
        self.method = method
        self.address = address
        self.params = params if params is not None else {}
        self.headers = headers if headers is not None else {}
        self.cookies = cookies if cookies is not None else {}
        self.valid = valid

    @staticmethod
    def get_invalid():
        return HttpRequest(Method.GET, '', valid=False)

    @staticmethod
    def from_bytes(data) -> HttpRequest:
        if data[-4:] != b'\r\n\r\n':
            return HttpRequest.get_invalid()
        text = data.decode().split('\r\n')[:-2]
        header_parsing = HttpRequest.parse_header(text[0])
        if header_parsing is None:
            return HttpRequest.get_invalid()
        method, addr, params, version = header_parsing
        headers = to_dictionary(map(lambda header: tuple(header.split(': ')),
                                    text[1:]))
        if 'Cookie' in headers:
            cookies = to_dictionary(map(
                lambda cookie: tuple(cookie.split('=')),
                headers['Cookie'].split('; ')))
            del headers['Cookie']
        else:
            cookies = {}
        if 'Connection' not in headers:
            if version == 'HTTP/1.0':
                headers['Connection'] = 'close'
            else:
                headers['Connection'] = 'keep-alive'
        return HttpRequest(method, addr, params, headers, cookies)

    @staticmethod
    def parse_header(header) \
            -> typing.Tuple[Method, str, typing.Dict[str, str], str] or None:
        header = header.split()
        if len(header) != 3 or (header[2] != 'HTTP/1.0'
                                and header[2] != 'HTTP/1.1'):
            return None
        try:
            method = Method(header[0])
        except ValueError:
            return None
        version = header[2]
        addr, params_str = (header[1].split('?')
                            if header[1].find('?') != -1
                            else (header[1], None))
        if params_str is not None:
            # noinspection PyUnresolvedReferences
            params = to_dictionary(map(lambda pair: tuple(pair.split('=')),
                                       params_str.split('&')))
        else:
            params = {}
        return method, addr, params, version
