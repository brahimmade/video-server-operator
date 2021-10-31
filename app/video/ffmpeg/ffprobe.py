import subprocess

from ast import literal_eval
from os import PathLike

from app.filesystem import path


def get_video_metadata(video_path: PathLike) -> dict:
    """
    Получить метаданные видео посредством ffprobe
    Args:
        video_path (PathLike): Путь до видео, из которого необходимо извлечь метаданные

    Returns:
        dict: Словарь метаданных видео

    Raises:
        FileNotFoundError, TypeError: Поднимается, если по передеанному пути не был найден файл
        subprocess.CalledProcessError: Если во время процесса поиска метаданных произошла ошибка
    """

    try:
        video_path = path.convert_to_pathlib(video_path, check_exist=True)
    except (FileNotFoundError, TypeError) as err:
        raise err

    command = [
        "ffprobe",
        video_path,
        "-loglevel", "quiet",
        "-print_format", "json",
        "-select_streams", "v:0",
        "-show_entries", "stream=duration,bit_rate,codec_name"
    ]

    try:
        result = subprocess.check_output(command)
        return literal_eval(result.decode())
    except subprocess.CalledProcessError as err:
        raise err
