from aiohttp import web
from app.utils.fpylog import Log
import asyncio

log = Log(file_log=True, file_log_name="api")


class Api:
    def __init__(self, host: str = '0.0.0.0', port: int = 5080):
        self.host = host
        self.port = port
        self.host_runners = []

        self.ROUTES = [
            web.get('/find_files', self._send_files)
        ]

    async def _send_files(self, request: web.Request):
        return web.Response(status=200)

    async def _start_new_site_runner(self, app: web.Application, host: str, port: int) -> None:
        """
        Создает новый раннер сервера
        Args:
            app (web.Application): aiohttp приложение сервера
            host (str): Название хоста
            port (int): Порт для запуска сервера

        Returns:
            None
        """
        runner = web.AppRunner(app)
        self.host_runners.append(runner)
        await runner.setup()
        site = web.TCPSite(runner, host, port)
        await site.start()
        log.success(f"Запущен сервер {host}:{port}", log_file=False)

    async def start(self):
        api_server = web.Application()
        async_loop = asyncio.get_event_loop()
        async_loop.create_task(self._start_new_site_runner(api_server, host=self.host, port=self.port))
