from __future__ import annotations
import typing
import re

from infrastructure.iterator_extensions import to_dictionary
from request.request_method import Method
from request.form_data import FormData
from request.form import Form


class HttpRequest:
    def __init__(self, method: Method,
                 address: str,
                 params: typing.Dict[str, str] = None,
                 headers: typing.Dict[str, str] = None,
                 cookies: typing.Dict[str, str] = None,
                 form: Form = None,
                 valid: bool = True,
                 complete: bool = True):
        self.method = method
        self.address = address
        self.params = params if params is not None else {}
        self.headers = headers if headers is not None else {}
        self.cookies = cookies if cookies is not None else {}
        self.form = form
        self.valid = valid

    @staticmethod
    def get_invalid():
        return HttpRequest(Method.GET, '', valid=False)

    @classmethod
    def from_bytes(cls, data: bytes) -> HttpRequest:
        if b'\r\n\r\n' not in data:
            return HttpRequest.get_invalid()
        data, form_data = (data[:data.find(b'\r\n\r\n') + 4],
                           data[data.find(b'\r\n\r\n') + 4:])
        text = data.decode().split('\r\n')[:-2]
        header_parsing = cls.parse_header(text[0])
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
        if 'Host' not in headers:
            host, addr = addr[:addr.find('/')], addr[addr.find('/'):]
            headers['Host'] = host
        if 'Connection' not in headers:
            if version == 'HTTP/1.0':
                headers['Connection'] = 'close'
            else:
                headers['Connection'] = 'keep-alive'
        if form_data == b'':
            return cls(method, addr, params, headers, cookies)
        content_type = headers.get('Content-Type')
        type_re = re.compile(r'^multipart/form-data; boundary=(----(.+))$')
        if (content_type is None
                or type_re.match(content_type) is None):
            raise ValueError("Incorrect content")
        form = cls.parse_form(form_data,
                              '--' + type_re.match(content_type).group(1
                                                                       ))
        return cls(method, addr, params, headers, cookies, form)

    @classmethod
    def parse_header(cls, header) \
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

    @classmethod
    def parse_form(cls, form_data: bytes, boundary: str):
        boundary = boundary.encode()
        print(boundary + b'--\r\n', form_data[-len(boundary) - 4:])
        if not form_data.endswith(boundary + b'--\r\n'):
            raise ValueError('Incorrect form data')
        blocks = form_data[:-len(boundary) - 4].split(boundary + b'\r\n')
        return Form(*list(map(FormData.from_bytes, blocks[1:])))


if __name__ == '__main__':
    req = HttpRequest.from_bytes(
        b'POST / HTTP/1.1\r\n'
        b'Host: myserver\r\n'
        b'Content-Type: multipart/form-data; boundary=----aaaaa\r\n'
        b'Content-Length: 1\r\n'
        b'\r\n'
        b'------aaaaa\r\n'
        b'Content-Disposition: form-data; name="name"\r\n'
        b'\r\n'
        b'a\r\n'
        b'------aaaaa--\r\n')
    print(req.method,
          req.address,
          req.params,
          req.headers,
          req.cookies,
          req.form,
          req.valid)
