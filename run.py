from ast import literal_eval
from os import environ
from app.cam_watchdog import CamWatchdog
from app.web.api import Api
from app.db import database
from app.utils import load_env_file


if __name__.endswith("__main__"):
    load_env_file()
    cam_watchdog = CamWatchdog(literal_eval(environ.get('CAM_SERVER_LIST')))
    api_server = Api(host=environ.get('API_SERVER_HOST'), port=int(environ.get('API_SERVER_PORT')))
    db = database.Database(user=environ.get('DB_USER'),
                           password=environ.get('DB_PASSWORD'),
                           database=environ.get('DB_NAME'),
                           host=environ.get('DB_HOST'))
    db.init()
