from ast import literal_eval
from os import environ
from app.cam_watchdog import CamWatchdog
from app.web.api import Api
from app.db import database
from app.utils import load_env_file
from asyncio import get_event_loop

if __name__.endswith("__main__"):
    load_env_file()
    cam_watchdog = CamWatchdog(literal_eval(environ.get('CAM_SERVER_LIST')))
    api_server = Api(host=environ.get('API_SERVER_HOST'), port=int(environ.get('API_SERVER_PORT')))
    db = database.Database(user=environ.get('DB_USER'),
                           password=environ.get('DB_PASSWORD'),
                           database=environ.get('DB_NAME'),
                           host=environ.get('DB_HOST'))

    async_loop = get_event_loop()

    async_loop.create_task(api_server.start())
    async_loop.create_task(cam_watchdog.start())
    async_loop.create_task(db.init())

    try:
        async_loop.run_forever()
    finally:
        for runner in api_server.host_runners:
            async_loop.run_until_complete(runner.cleanup())
