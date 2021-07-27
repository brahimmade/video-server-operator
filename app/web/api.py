from aiohttp import web


class Api:
    def __init__(self, host: str = '0.0.0.0', port: int = 5080):
        self.host = host
        self.port = port
        self.ROUTES = [
            web.get('/find_files', self._send_files)
        ]

    async def _send_files(self, request: web.Request):
        breakpoint()
        return web.Response(status=200)

    def start(self):
        web_app = web.Application()

        web.run_app(web_app, host=self.host, port=self.port)