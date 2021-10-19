import datetime

from typing import Union, List
from pydantic import BaseModel


class SearchFiles(BaseModel):
    """Модель PyDantic для поиска файлов по заданными критериям"""
    server: Union[str, int]
    camera: Union[str, int, List[str], List[int]]
    datetime_start: datetime.datetime
    datetime_end: datetime.datetime
