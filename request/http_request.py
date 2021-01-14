import re
import typing

from request.form import Form
from request.form_data import FormData
from request.request_method import Method


class HttpRequest:
    def __init__(self, method: Method,
                 address: str,
                 params: typing.Dict[str, str] = None,
                 headers: typing.Dict[str, str] = None,
                 cookies: typing.Dict[str, str] = None,
                 form: Form = None,
                 valid: bool = True):
        self.method = method
        self.address = address
        self.params = params or {}
        self.headers = headers or {}
        self.cookies = cookies or {}
        self.form = form
        self.valid = valid

    @staticmethod
    def get_invalid():
        return HttpRequest(Method.GET, '', valid=False)

    @classmethod
    def from_bytes(cls, data: bytes):
        if b'\r\n\r\n' not in data:
            return HttpRequest.get_invalid()
        data, form_data = (data[:data.find(b'\r\n\r\n') + 4],
                           data[data.find(b'\r\n\r\n') + 4:])
        text = data.decode().split('\r\n')[:-2]
        header_parsing = cls.parse_header(text[0])
        if header_parsing is None:
            return HttpRequest.get_invalid()
        method, addr, params, version = header_parsing
        headers = dict(map(lambda header: tuple(header.split(': ')),
                           text[1:]))
        if 'Cookie' in headers:
            cookies = dict(map(
                lambda cookie: (cookie[:cookie.find('=')],
                                cookie[cookie.find('=') + 1:]),
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
            params = dict(map(lambda pair: tuple(pair.split('=')),
                              params_str.split('&')))
        else:
            params = {}
        return method, addr, params, version

    @classmethod
    def parse_form(cls, form_data: bytes, boundary: str):
        boundary = boundary.encode()
        if not form_data.endswith(boundary + b'--\r\n'):
            raise ValueError('Incorrect form data')
        blocks = form_data[:-len(boundary) - 4].split(boundary + b'\r\n')
        return Form(*list(map(FormData.from_bytes, blocks[1:])))
