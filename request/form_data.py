import re


class FormData:
    def __init__(self, name, data: bytes, file_name: str = None,
                 file_type: str = None):
        self.name = name
        self.file_name = file_name
        self.data = data
        self.file_type = file_type

    @classmethod
    def from_bytes(cls, data: bytes):
        header_end = data.find(b'\r\n\r\n')
        header = data[:header_end].decode()
        content = data[header_end + 4:-2]
        no_file = re.compile(r'^Content-Disposition: form-data; '
                             r'name="([^"]+)"$')
        match = no_file.match(header)
        if match is not None:
            groups = match.groups()
            name = groups[0]
            return cls(name, content)
        file = re.compile(r'^Content-Disposition: form-data; '
                          r'name="([^"]+)"; '
                          r'filename="([^"]+)"\r\n'
                          r'Content-Type: ([^\r]+)$')
        match = file.match(header)
        if match is not None:
            groups = match.groups()
            name = groups[0]
            file_name = groups[1]
            file_type = groups[2]
            return cls(name, content, file_name, file_type)

        raise ValueError("Incorrect data")

    def __eq__(self, other):
        if not isinstance(other, FormData):
            return False
        return (self.name == other.name
                and self.data == other.data
                and self.file_name == other.file_name
                and self.file_type == other.file_type)
