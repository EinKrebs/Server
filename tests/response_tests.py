import unittest

from response.http_response import HttpResponse
from response.response_code import Code


def test_text_data_params(data):
    resp = HttpResponse(text_data=data)
    return (resp.to_bytes().decode(),
            'HTTP/1.1 200 OK\r\n'
            'Server: python\r\n'
            'Content-Type: text/html; charset=UTF-8\r\n'
            f'Content-Length: {len(data.encode())}\r\n'
            '\r\n'
            f'{data}')


class HttpResponseTests(unittest.TestCase):
    def test_code(self):
        resp = HttpResponse(Code.OK)
        self.assertEqual(resp.to_bytes().decode(),
                         'HTTP/1.1 200 OK\r\n'
                         'Server: python\r\n'
                         '\r\n')
        resp = HttpResponse(Code.PAGE_NOT_FOUND)
        self.assertEqual(resp.to_bytes().decode(),
                         'HTTP/1.1 404 Not Found\r\n'
                         'Server: python\r\n'
                         '\r\n')

    def test_different_data(self):
        self.assertEqual(*test_text_data_params(
            'sjdfsljkhfkajshfkbasdygaskbd;aba/wdfjbaslydfgbbd'))
        self.assertEqual(*test_text_data_params(
            'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'))
