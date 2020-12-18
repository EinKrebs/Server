import asyncio
import os

from server import Server


async def main():
    server = Server()

    @server.file('/')
    def filename(request):
        return f'{os.getcwd()}/example'

    @server.directory_listing('/files')
    def directory(request):
        return '/home/krebs/PythonProjects/Server'

    await server.start()


if __name__ == '__main__':
    asyncio.run(main())
