import asyncio
import os
import datetime
from PIL import Image

from server import Server
from request.http_request import HttpRequest
from request.request_method import Method
from response.http_response import HttpResponse
import html_functions
from html_functions import HtmlFormField as field,\
    HtmlFormFieldType as field_type


def file_from_dictionary(dictionary: dict, boundary: bytes, path: str):
    with open(path, 'wb') as f:
        f.write(b'boundary=' + boundary + b'\n')
        for key, value in dictionary.items():
            f.write(boundary + key.encode() + b'\n' + value)


def view_func(addr: str):
    def res(file_name: str):
        if file_name[file_name.rfind('/') + 1:] == 'file_data':
            return ''
        try:
            dictionary = dictionary_from_file(file_name)
        except ValueError:
            return ''
        full_name = file_name
        file_name = dictionary["file_name"]
        size = tuple(dictionary['size'].split('x'))
        result = html_functions.href(f'{addr}/{file_name}',
                                     file_name) + ':<br>'
        result += html_functions.image('/file_data/' + file_name,
                                       file_name, size) + '<br>'
        for key, value in dictionary.items():
            if key == 'file' or key == 'file_name':
                continue
            result += f'{key}: {value}<br>'
        return result
    return res


def dictionary_from_file(path):
    with open(path, 'rb') as f:
        content = f.read()
    if not content.startswith(b'boundary='):
        raise ValueError
    boundary = content[9:content.find(b'\n')]
    index = content.find(b'\n') + 1 + len(boundary)
    res = {}
    while index < len(content):
        name = content[index:content.find(b'\n', index)].decode()
        index += len(name) + 1
        value_end = content.find(boundary, index)
        if value_end == -1:
            value_end = len(content)
        value = content[index:value_end].decode()
        index = value_end + len(boundary)
        res[name] = value
    return res


async def main():
    server = Server()
    os.chdir('./demo')

    if 'files' not in os.listdir():
        os.mkdir(os.getcwd() + '/files')
    if 'file_data' not in os.listdir(os.getcwd() + '/files'):
        os.mkdir(os.getcwd() + '/files/file_data')
    for file in os.listdir(os.getcwd() + '/files/file_data'):

        @server.file('/file_data/' + file, const=True)
        def func(request):
            return os.getcwd() + '/files/file_data/' + file

    @server.directory_listing(
        '/file_data',
        view=view_func(f'file_data'))
    def directory(request):
        return '/home/krebs/PythonProjects/Server/demo/files'

    @server.custom_handler('/')
    def uploader(request: HttpRequest):
        if request.method == Method.POST:
            os.chdir(os.getcwd() + '/files')
            if 'file_data' not in os.listdir():
                os.mkdir(os.getcwd() + '/file_data')
            files = request.form.file_fields.values()
            if len(files) != 1:
                raise ValueError("Incorrect file number")

            if ('name' not in request.form.text_fields
                    or 'description' not in request.form.text_fields):
                raise ValueError("Incorrect form data")

            dictionary = {
                'name': request.form.text_fields['name'].data,
                'description': request.form.text_fields['description'].data}

            file = request.form.file_fields['photo']
            file.file_name = file.file_name.replace(' ', '_')

            if file.file_name in os.listdir():
                raise ValueError("file already exists")
            with open(file.file_name, 'wb') as f:
                f.write(file.data)
            try:
                image = Image.open(file.file_name)
                image.verify()
            except IOError:
                raise ValueError("file is not an image")
            os.remove(file.file_name)

            if image.size is None:
                size = b'Undefined'
            else:
                size = f'{image.size[0]}x{image.size[1]}'.encode()
            date = datetime.date.today()
            date = f'{date.day}/{date.month}/{date.year}'.encode()
            dictionary['size'] = size
            dictionary['date'] = date
            dictionary['file_name'] = file.file_name.encode()

            file_from_dictionary(dictionary,
                                 b'----asdnmjanda8asdnd/*1amsd',
                                 f'{os.getcwd()}/{file.file_name}.meta')
            with open(os.getcwd() + '/file_data/' + file.file_name, 'wb') as f:
                f.write(file.data)

            @server.file('/file_data/' + file.file_name, const=True)
            def file_data(request):
                return os.getcwd() + '/file_data/' + file.file_name

            os.chdir('..')

        return HttpResponse(
            text_data=html_functions.form('Upload an image',
                                          '/',
                                          field('name', field_type.Text),
                                          field('photo', field_type.File),
                                          field('description',
                                                field_type.Text),
                                          field('', field_type.Submit))
            + 'You can see and download images '
            + html_functions.href('/file_data', 'here'))

    await server.start()

if __name__ == '__main__':
    asyncio.run(main())
