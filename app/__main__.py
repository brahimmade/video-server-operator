from ast import literal_eval
from os import environ
from app.filesystem import Watchdog
from app.web.api import Api
from asyncio import get_event_loop


def run() -> None:
    """Запуск проекта"""
    filesystem_watchdog = Watchdog(literal_eval(environ.get('ARCHIVES_LIST')))
    api_server = Api(host=environ.get('API_SERVER_HOST'), port=int(environ.get('API_SERVER_PORT')))

    filesystem_watchdog.start()

    async_loop = get_event_loop()
    async_loop.create_task(api_server.start())

    try:
        async_loop.run_forever()
    finally:
        for runner in api_server.host_runners:
            async_loop.run_until_complete(runner.cleanup())


if __name__ == "__main__":
    run()
