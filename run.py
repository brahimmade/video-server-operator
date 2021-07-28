from ast import literal_eval
from pathlib import Path
from dotenv import get_key as env_get_key
from sys import path as sys_path

from app.cam_watchdog import CamWatchdog
from app.web.api import Api
from app.utils import exit_with_error_message


def _load_env_file(env_file: str = 'config.env') -> Path:
    """
    Возвращает путь до config.env файла, если его нет, то создает новый
    :return:
    """
    dotenv_path = Path(f"{sys_path[0]}/{env_file}")
    return dotenv_path if dotenv_path.exists() else exit_with_error_message(
        f"Невозможно прочитать файл с конфигурацией {env_file}!")


if __name__.endswith("__main__"):
    env = _load_env_file()
    cam_watchdog = CamWatchdog(literal_eval(env_get_key(env, 'CAM_SERVER_LIST')))
    api_server = Api(host=env_get_key(env, 'API_SERVER_HOST'), port=int(env_get_key(env, 'API_SERVER_PORT')))
