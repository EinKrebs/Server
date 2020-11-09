from .response_code import Code


class HttpResponse:
    def __init__(self, code: Code = Code.OK, text_data: bytes = None):
        self.code = code
        self.text_data = text_data

    def to_bytes(self):
        result = f'HTTP/1.1 {self.code[0]} {self.code[1]}\r\n'
        if self.text_data:
            result += f'Content-Type: text/html; charset=UTF-8\r\n' \
                      f'Content-Length: {len(self.text_data)}\r\n' \
                      f'\r\n' \
                      f'{self.text_data}\r\n'
        return result
