import unittest
import random

from request.form_data import FormData
from request.form import Form


class FormTests(unittest.TestCase):
    def test_general(self):
        random.seed(100)
        text_fields = [FormData(str(random.random()),
                                str(random.random()).encode())
                       for _ in range(5000)]
        file_fields = [FormData(str(random.random()),
                                str(random.random()).encode(),
                                str(random.random()),
                                'text/html')
                       for _ in range(5000)]
        form = Form(*(text_fields + file_fields))
        for field in text_fields:
            self.assertIsNotNone(form.text_fields.get(field.name))
            self.assertIsNone(form.file_fields.get(field.name))
            self.assertEqual(form.text_fields.get(field.name), field)

        for field in file_fields:
            self.assertIsNone(form.text_fields.get(field.name))
            self.assertIsNotNone(form.file_fields.get(field.name))
            self.assertEqual(form.file_fields.get(field.name), field)
