import os
import platform

from datetime import datetime
from pathlib import Path


def modification_date(path_to_file: [str, Path]) -> datetime:
    """
    Получить точное время изменения файла
    Args:
        path_to_file (str | Path): Путь до файла, для которого необходимо найти время изменения

    Returns:
        datetime: Полное время изменения
    """
    stat = os.stat(path_to_file)
    modification_timestamp = os.path.getmtime(path_to_file) if platform.system() == 'Windows' else stat.st_mtime

    return datetime.fromtimestamp(modification_timestamp)
