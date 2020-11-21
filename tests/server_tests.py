import unittest

from server import Server
from response.http_response import HttpResponse
from response.response_code import Code


class ServerTests(unittest.TestCase):
    def test_handle_request(self):
        server = Server()
        server.handlers['a'] = lambda req: HttpResponse(text_data=b'first')
        server.handlers['b'] = lambda req: HttpResponse(text_data=b'second')
        first_resp = server.handle_request(b'GET a HTTP/1.0\r\n\r\n')
        self.assertEqual(first_resp.code, Code.OK)
        self.assertEqual(first_resp.text_data, b'first')
        second_resp = server.handle_request(b'GET b HTTP/1.0\r\n\r\n')
        self.assertEqual(second_resp.code, Code.OK)
        self.assertEqual(second_resp.text_data, b'second')
        self.assertEqual(server.handle_request(b'GET c HTTP/1.0\r\n\r\n').code,
                         Code.PAGE_NOT_FOUND)
