import asyncio

from server import Server


async def main():
    server = Server()

    @server.text('/hw')
    def a(request):
        return 'Hello world'

    await server.start()


if __name__ == '__main__':
    asyncio.run(main())
