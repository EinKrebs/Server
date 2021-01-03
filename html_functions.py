from enum import Enum
from typing import List
from PIL import Image


def base_structure(title, content):
    return ('<!DOCTYPE html>\n' 
            '<html>\n'
            '<head>'
            f'<title>{title}</title>\n'
            '</head>\n'
            '<body>\n'
            f'{content}'
            '</body>\n'
            '</html>')


def block(elem_name, content):
    return f'<{elem_name}>\n{content}\n</{elem_name}>\n'


def wrap(elem_name, content):
    return f'<{elem_name}>{content}</{elem_name}>\n'


class HtmlFormFieldType(Enum):
    Text = 'text'
    File = 'file'
    Submit = 'submit'


class HtmlFormField:
    def __init__(self, name: str, field_type: HtmlFormFieldType):
        self.name = name
        self.type = field_type

    def to_html(self):
        return wrap('p',
                    f'<input type="{self.type.value}" name="{self.name}">')


def _contains_file(fields: List[HtmlFormField]):
    for field in fields:
        if field.type == HtmlFormFieldType.File:
            return True
    return False


def form(title: str, action: str, *fields: HtmlFormField):
    return base_structure(
        '',
        f'<form action="{action}" method="POST"'
        + (' enctype="multipart/form-data"'
           if _contains_file(list(fields))
           else '')
        + f'>\n{wrap("h1", title)}\n'
        + "\n".join(
            f'<label for="{field.name}">{field.name}</label>'
            f' {HtmlFormField.to_html(field)}'
            for field in fields)
        + '\n</form>')


def href(addr, name):
    return f'<a href="{addr}">{name}</a>'


def image(path, alt_text, size=None):
    if size is None:
        img = Image.open(path)
        size = img.size
    if len(size) != 2:
        raise ValueError("Incorrect image size")
    width = size[0]
    height = size[1]
    return f'<img src="{path}" alt="{alt_text}" width="{width}" ' \
           f'height = "{height}">'
