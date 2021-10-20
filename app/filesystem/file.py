import os
import platform

from datetime import datetime


def modification_date(path_to_file: os.PathLike) -> datetime:
    """
    Получить точное время изменения файла
    Args:
        path_to_file (os.PathLike): Путь до файла, для которого необходимо найти время изменения

    Returns:
        datetime: Полное время изменения
    """
    stat = os.stat(path_to_file)
    modification_timestamp = os.path.getmtime(path_to_file) if platform.system() == 'Windows' else stat.st_mtime

    return datetime.fromtimestamp(modification_timestamp)
