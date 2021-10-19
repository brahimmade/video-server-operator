from fastapi import APIRouter
from starlette import requests, responses

from . import logic, models

router = APIRouter()


@router.get('/search_files', responses={202: {"description": "Operation forbidden"}})
async def search_files(_: requests.Request, search_data: models.SearchFiles) -> responses.JSONResponse:
    """
    Получить файлы с камер по заданным параметрам
    Args:
        _ (requests.Request): Входящий запрос
        search_data (models.SearchFiles): Параметры для поиска файлов видео

    Returns:
        responses.JSONResponse: JSON ответ с данными видео-файлов
    """
    return logic.search_files(search_data=search_data)
