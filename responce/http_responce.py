from .response_code import Code


class HttpResponse:
    def __init__(self, code: Code = Code.OK, text_data: bytes = None):
        self.code = code
        self.text_data = text_data

    def to_bytes(self):
        t = self.code.value
        result = f'HTTP/1.1 {t[0]} {t[1]}\r\n' \
                 f'Server: python\r\n'
        if self.text_data:
            result += f'Content-Type: text/html; charset=UTF-8\r\n' \
                      f'Content-Length: {len(self.text_data)}\r\n' \
                      f'\r\n' \
                      f'{self.text_data}'
        else:
            result += '\r\n'
        return result.encode()
