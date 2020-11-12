from enum import Enum


class Code(Enum):
    OK = (200, "OK")
    PAGE_NOT_FOUND = (404, "Not Found")
