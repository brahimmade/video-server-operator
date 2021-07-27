from ast import literal_eval
from os import path
from dotenv import get_key as env_get_key
from sys import path as sys_path

from app.cam_watchdog import CamWatchdog
from app.web.api import Api


def _setup_env_file() -> str:
    pass


def _load_env_data() -> str:
    """
    Запись переменных окружения из config.env в окружение python
    :return:
    """
    dotenv_path = path.join(sys_path[0], 'config.env')
    return dotenv_path if path.exists(dotenv_path) else _setup_env_file()


if __name__.endswith("__main__"):
    env = _load_env_data()
    cam_watchdog = CamWatchdog([server for server in literal_eval(env_get_key(env, 'cam_server_list'))])
    api_server = Api(host=env_get_key(env, 'API_SERVER_HOST'), port=int(env_get_key(env, 'API_SERVER_PORT')))
