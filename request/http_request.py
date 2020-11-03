import typing
from .request_method import Method
from infrastructure.iterator_extensions import (to_dictionary,
                                                dictionary_to_string)


class HttpRequest:
    def __init__(self, method: Method, address: str,
                 params: typing.Dict[str, str],
                 headers: typing.Dict[str, str],
                 cookies: typing.Dict[str, str]):
        self.method = method
        self.address = address
        self.params = params
        self.headers = headers
        self.cookies = cookies

    @staticmethod
    def from_bytes(data):
        text = data.decode().split('\r\n')
        a = text[0].split()
        method = a[0]
        addr, params_str = a[1].split('?')
        params = to_dictionary(map(lambda pair: tuple(pair.split('=')),
                                   params_str.split('&')))
        headers = to_dictionary(map(lambda header: tuple(header.split(': ')),
                                    text[1:]))
        if 'Cookie' in headers:
            cookies = to_dictionary(map(lambda cookie: tuple(cookie.split('=')),
                                        headers['Cookie'].split('&')))
            del headers['Cookie']
        else:
            cookies = {}
        if 'Host' not in headers:
            # TODO: test this
            host, address = addr[:addr.find('/')], addr[addr.find('/'):]
            headers['Host'] = host
            addr = address
        return HttpRequest(method, addr, params, headers, cookies)

    def to_bytes(self):
        res = str(self.method)
        res += f' {self.address}'
        if len(self.params) != 0:
            res += f'?{dictionary_to_string(self.params, "&", "=")}'
        res += ' HTTP/1.1\r\n'
