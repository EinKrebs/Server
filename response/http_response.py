from response.response_code import Code


class HttpResponse:
    def __init__(self, code: Code = Code.OK, text_data: bytes = None,
                 file: str = None):
        self.code = code
        self.text_data = text_data
        self.file = file

    def to_bytes(self):
        t = self.code.value
        result = (f'HTTP/1.1 {t[0]} {t[1]}\r\n' 
                  f'Server: python\r\n').encode()
        if self.text_data:
            result += (f'Content-Type: text/html; charset=UTF-8\r\n' 
                       f'Content-Length: {len(self.text_data)}\r\n' 
                       f'\r\n' 
                       f'{self.text_data}').encode()
            result += b'\r\n'
            return result
        if self.file:
            with open(self.file, 'rb') as f:
                content = f.read()
                result += (f'Content-Type: application/octet-stream\r\n' 
                           f'Content-Length: {len(content)}\r\n\r\n').encode()
                result += content

        result += b'\r\n'
        return result
