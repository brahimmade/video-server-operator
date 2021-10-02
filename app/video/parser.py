from datetime import datetime
from typing import TypedDict

from pathlib import Path

from app.filesystem import file, path
from .ffmpeg import ffprobe


class VideoData(TypedDict):
    """Объект с данными видео-файла"""
    name: str
    time: datetime
    extension: str
    duration: float
    bitrate: int
    codec: str


def get_video_data(video_path: [str, Path]) -> VideoData:
    """
    Получить данные о переданном видео-файле
    Args:
        video_path (str | Path): Путь до необходимого видео-файла

    Returns:
        VideoData: Словарь данных о видео
    """

    try:
        video_path = path.convert_to_pathlib(video_path, check_exist=True)
    except (FileNotFoundError, TypeError) as err:
        raise err

    video_metadata = ffprobe.get_video_metadata(video_path=video_path)

    video_file_data = {
        'name': video_path.stem,
        'extension': video_path.suffix,
        'time': file.modification_date(video_path)
    }
    video_data = VideoData(
        **video_file_data,
        duration=float(video_metadata.get('streams')[0].get('duration')),
        bitrate=video_metadata.get('streams')[0].get('bit_rate'),
        codec=video_metadata.get('streams')[0].get('codec_name')
    )

    return video_data
