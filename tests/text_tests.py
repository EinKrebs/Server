import unittest

from server import Server
from request.http_request import HttpRequest
from request.request_method import Method
from response.http_response import HttpResponse


class TextTests(unittest.TestCase):
    def simple_test(self):
        server = Server()

        @server.text('page')
        def test_func(request):
            return 'test'

        response = test_func(HttpRequest(Method.GET, 'page'))
        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.text_data, b'test')
