import unittest

from request.http_request import HttpRequest
from request.request_method import Method


class HttpRequestTests(unittest.TestCase):
    def assert_invalid(self, data):
        try:
            req = HttpRequest.from_bytes(data)
        except Exception:
            self.fail()
        self.assertFalse(req.valid)

    def test_incorrect_method(self):
        data = 'WRONG_METHOD / HTTP/1.1\r\nHost: myserver\r\n\r\n'
        self.assert_invalid(data.encode())

    def test_incorrect_version(self):
        data = 'GET / ICMP\r\nHost: myserver\r\n\r\n'
        self.assert_invalid(data.encode())

    def test_incorrect_header(self):
        data = 'TWO WORDS\r\nHost: abc\r\n'
        self.assert_invalid(data.encode())
        data = 'F O U R\r\nHost:abc\r\n'
        self.assert_invalid(data.encode())

    def test_incomplete(self):
        data = 'GET / HTTP/1.1\r\nHost: abc\r\n'
        self.assert_invalid(data.encode())

    def test_no_host(self):
        data = 'GET / HTTP/1.1\r\n\r\n'
        self.assert_invalid(data.encode())

    def test_method(self):
        data = 'GET 127.0.0.1/ HTTP/1.0\r\n\r\n'
        req = HttpRequest.from_bytes(data.encode())
        self.assertEqual(req.method, Method.GET)

    def test_host_and_address(self):
        data = 'GET localhost/right_address HTTP/1.0\r\n\r\n'
        req = HttpRequest.from_bytes(data.encode())
        self.assertTrue(req.valid)
        self.assertEqual(req.address, '/right_address')
        self.assertEqual(req.headers['Host'], 'localhost')
        data = 'GET /right_address HTTP/1.1\r\nHost: localhost\r\n\r\n'
        req = HttpRequest.from_bytes(data.encode())
        self.assertTrue(req.valid)
        self.assertEqual(req.address, '/right_address')
        self.assertEqual(req.headers['Host'], 'localhost')

    def test_params(self):
        data = 'GET /addr?a=1&b=param_b&c=abracadabra HTTP/1.1\r\n' \
               'Host: abc\r\n' \
               '\r\n'
        req = HttpRequest.from_bytes(data.encode())
        self.assertTrue(req.valid)
        self.assertDictEqual(req.params, {'a': '1', 'b': 'param_b',
                                          'c': 'abracadabra'})

    def test_headers(self):
        data = 'GET /addr HTTP/1.1\r\n' \
               'Host: abc\r\n' \
               'a: 1\r\n' \
               'b: header_b\r\n' \
               'c: lorem ipsum\r\n' \
               '\r\n'
        req = HttpRequest.from_bytes(data.encode())
        self.assertTrue(req.valid)
        self.assertDictEqual(req.headers, {'a': '1', 'b': 'header_b',
                                           'c': 'lorem ipsum', 'Host': 'abc'})

    def test_cookies(self):
        data = 'GET /addr HTTP/1.1\r\n' \
               'Host: abc\r\n' \
               'Cookie: a=1; b=cookie_b; c=lorem ipsum\r\n' \
               '\r\n'
        req = HttpRequest.from_bytes(data.encode())
        self.assertTrue(req.valid)
        self.assertDictEqual(req.cookies, {'a': '1', 'b': 'cookie_b',
                                          'c': 'lorem ipsum'})
