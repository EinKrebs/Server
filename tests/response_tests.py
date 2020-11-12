import unittest

from response.http_response import HttpResponse
from response.response_code import Code


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
        self.test_text_data('sjdfsljkhfkajshfkbasdygaskbd;aba/wdfjbaslydfgbbd')
        self.test_text_data('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')

    @unittest.skip("method can be used only in other methods")
    def test_text_data(self, data):
        resp = HttpResponse(text_data=data)
        self.assertEqual(resp.to_bytes().decode(),
                         'HTTP/1.1 200 OK\r\n'
                         'Server: python\r\n'
                         'Content-Type: text/html; charset=UTF-8\r\n'
                         f'Content-Length: {len(data.encode())}\r\n'
                         '\r\n'
                         f'{data}')
