from typing import AnyStr

import uvicorn

from fastapi import FastAPI
from . import api

web = FastAPI()

web.include_router(router=api.router)


def run(host: AnyStr = 'localhost', port: int = 5800) -> None:
    """
    Запустить работу web сервера uvicorn посредством кода

    Args:
        host (AnyStr): Хост, для которого будет запущен сервер uvicorn
        port (int): Порт сервера
    """
    uvicorn.run(web, host=host, port=port, log_level="debug")
