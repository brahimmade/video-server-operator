import subprocess

from ast import literal_eval

from pathlib import Path

from app.filesystem import path


def get_video_metadata(video_path: [str, Path]) -> dict:
    """
    Получить метаданные видео посредством ffprobe
    Args:
        video_path (str | Path): Путь до видео, из которого необходимо извлечь метаданные

    Returns:
        dict: Словарь метаданных видео
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
        "-show_format",
        "-show_streams"
    ]

    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, check=True)

        if result.stderr:
            raise OSError(result.stderr)

        return literal_eval(result.stdout.decode())
    except (OSError, IOError) as err:
        raise err
