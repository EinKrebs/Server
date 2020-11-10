import typing
import sys

from .request_method import Method
from infrastructure.iterator_extensions import (to_dictionary,
                                                dictionary_to_string)


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
        return HttpRequest(Method.GET, '', {}, {}, {}, False)

    @staticmethod
    def from_bytes(data):
        if data[-4:] != b'\r\n\r\n':
            return HttpRequest.get_invalid()
        text = data.decode().split('\r\n')[:-2]
        a = text[0].split()
        if len(a) != 3 or (a[2] != 'HTTP/1.0' and a[2] != 'HTTP/1.1'):
            return HttpRequest.get_invalid()
        try:
            method = Method(a[0])
        except ValueError as e:
            print('Unknown request method', e, file=sys.stderr)
            return HttpRequest.get_invalid()
        version = a[2]
        addr, params_str = (a[1].split('?')
                            if a[1].find('?') != -1
                            else (a[1], None))
        if params_str is not None:
            # noinspection PyUnresolvedReferences
            params = to_dictionary(map(lambda pair: tuple(pair.split('=')),
                                       params_str.split('&')))
        else:
            params = {}
        headers = to_dictionary(map(lambda header: tuple(header.split(': ')),
                                    text[1:]))
        if 'Cookie' in headers:
            cookies = to_dictionary(map(lambda cookie: tuple(cookie.split('=')),
                                        headers['Cookie'].split('; ')))
            del headers['Cookie']
        else:
            cookies = {}
        if 'Host' not in headers:
            if version == 'HTTP/1.0':
                # TODO: test this
                host, address = addr[:addr.find('/')], addr[addr.find('/'):]
                headers['Host'] = host
                addr = address
            else:
                return HttpRequest.get_invalid()
        return HttpRequest(method, addr, params, headers, cookies)

    def to_bytes(self):  # зачем мне это?
        res = str(self.method)
        res += f' {self.address}'
        if len(self.params) != 0:
            res += f'?{dictionary_to_string(self.params, "&", "=")}'
        res += ' HTTP/1.1\r\n'
        res += dictionary_to_string(self.headers, ': ', '\r\n')
        res += f'Cookie: {dictionary_to_string(self.cookies, "=", "; ")}\r\n'
        res += '\r\n'
        return res
