import asyncio
import os

from server import Server


async def main():
    server = Server()

    @server.file('/')
    def filename(request):
        return f'{os.getcwd()}/example'

    await server.start()


if __name__ == '__main__':
    asyncio.run(main())
