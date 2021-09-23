from ast import literal_eval
from os import environ
from app.cam_watchdog import CamWatchdog
from app.web.api import Api
from asyncio import get_event_loop


CAM_WATCHDOG = CamWatchdog(literal_eval(environ.get('CAM_SERVER_LIST')))
API_SERVER = Api(host=environ.get('API_SERVER_HOST'), port=int(environ.get('API_SERVER_PORT')))


def run() -> None:
    """Запустить проект"""
    async_loop = get_event_loop()

    async_loop.create_task(API_SERVER.start())
    async_loop.create_task(CAM_WATCHDOG.start())

    try:
        async_loop.run_forever()
    finally:
        for runner in API_SERVER.host_runners:
            async_loop.run_until_complete(runner.cleanup())


if __name__ == "__main__":
    run()
