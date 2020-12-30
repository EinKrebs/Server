import unittest
import random

from request.form_data import FormData


class FormDataTests(unittest.TestCase):
    def test_text_data(self):
        random.seed(100)
        for _ in range(100000):
            name = str(random.random())
            value = str(random.random())
            data = f'Content-Disposition: form-data; name="{name}"\r\n\r\n' \
                   f'{value}\r\n'.encode()
            form_data = FormData.from_bytes(data)
            self.assertEqual(form_data.name, name)
            self.assertEqual(form_data.data, value.encode())
            self.assertIsNone(form_data.file_type)
            self.assertIsNone(form_data.file_name)

    def test_file_data(self):
        random.seed(100)
        for _ in range(100000):
            name = str(random.random())
            file_name = str(random.random())
            file_type = 'text/html'
            file_data = str(random.random())
            data = f'Content-Disposition: form-data; name="{name}"; ' \
                   f'filename="{file_name}"\r\n' \
                   f'Content-Type: {file_type}\r\n\r\n' \
                   f'{file_data}\r\n'.encode()
            form_data = FormData.from_bytes(data)
            self.assertEqual(form_data.name, name)
            self.assertEqual(form_data.data, file_data.encode())
            self.assertEqual(form_data.file_type, file_type)
            self.assertEqual(form_data.file_name, file_name)
