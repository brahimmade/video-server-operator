import pathlib
import re

from datetime import datetime

from app.database import video_server


def split_path(path: [str, pathlib.Path], regexp: str = None) -> dict:
    """
    Разделяет строку на директории для базы данныъх
    Args:
        path (str, pathlib.Path): Путь для разделения
        regexp (str): Кастомное регулярное выражение для поиска путей

    Returns:
        dict: Возвращает словарь с ключами для базы данных

    Raises:
        ValueError: Вернет ошибку, если путь не соответсвует регулярному выражению
    """
    path = str(path).replace('\\', '/')  # Приведение к типу и нормальному формату пути

    regexp_server_dir = r'(\/?.+)$'  # Регулярка путь до сервера
    regexp_cam_dir = regexp_server_dir[:-1] + r'\/(\w+\-\d+)$'  # Регулярка путь до камеры на сервере
    regexp_video_dir = regexp_cam_dir[:-1] + r'\/(\d{4}\-\d{2}\-\d{2}\/.+)$'  # Регулярка путь до папки с видео
    regexp_video_file = regexp_video_dir[:-1] + r'\/(.+\.mp4|avi)$'  # Полный путь

    # Выбрать необходимую регулярку в зависимости от пути
    regexp = regexp if regexp is not None \
        else regexp_video_file if re.match(regexp_video_file, path) is not None \
        else regexp_video_dir if re.match(regexp_video_dir, path) is not None \
        else regexp_cam_dir if re.match(regexp_cam_dir, path) is not None \
        else regexp_server_dir
    try:
        split_path_dict = re.findall(regexp, path)
        return {
            'server': split_path_dict[0],
            'camera': split_path_dict[1] if len(split_path_dict) >= 2 else None,
            'video_path': split_path_dict[2] if len(split_path_dict) >= 3 else None,
            'video': split_path_dict[3] if len(split_path_dict) >= 4 else None
        }
    except IndexError:
        raise ValueError(f"Путь {path} - не соотвествует регулярному выражению")


def set_server(server_path: str) -> video_server.VideoServer:
    """
    Добавить в базу данных путь до сервера
    Args:
        server_path (str): Путь до сервера

    Returns:
        video_server.VideoServer: Модель добавленного сервера
    """
    server = video_server.set_or_get_new_server(server_dir=server_path)
    return server


def set_camera(camera_path: str, server: video_server.VideoServer) -> video_server.Camera:
    """
    Добавить в базу данных данные камеры
    Args:
        camera_path (str): Путь до камеры
        server (video_server.VideoServer): Модель VideoServer, которой будет привязана камера

    Returns:
        video_server.Camera: Модель добавленной камеры
    """
    camera = video_server.set_or_get_new_camera(camera_dir=camera_path,
                                                server=server)

    return camera


def set_video_path(video_path: str, camera: video_server.Camera) -> video_server.Camera:
    """
    Добавить в базу данных данные камеры
    Args:
        video_path (str): Путь до видео
        camera (video_server.Camera): Модель Camera, которой принадлежит видео

    Returns:
        video_server.VideoPath: Модель добавленного пути до видео
    """

    try:
        datestamp = re.findall(r'(\d{4}\-\d{2}\-\d{2})', video_path)[0]
    except IndexError:
        raise ValueError(f"Переданный путь {video_path} - не содержит даты или она некорректна")

    video_path = video_server.set_or_get_new_video_path(camera=camera,
                                                        video_path=video_path,
                                                        datestamp=datetime.strptime(datestamp, "%Y-%m-%d"))
    return video_path
