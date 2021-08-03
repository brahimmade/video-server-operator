import pathlib
import re


def split_path(video_path: [str, pathlib.Path], regexp: str = None) -> dict:
    """
    Разделяет строку на директории для базы данныъх
    Args:
        video_path (str, pathlib.Path): Путь до видео
        regexp (str): Кастомное регулярное выражение для поиска путей

    Returns:
        dict: Возвращает словарь с ключами для базы данных

    Raises:
        ValueError: Вернет ошибку, если путь не соответсвует регулярному выражению
    """
    video_path = str(video_path).replace('\\', '/')  # Приведение к типу и нормальному формату пути
    regexp = r'^(\/?.+)\/(.+\d+)\/(\d{4}\-\d{2}\-\d{2}\/.+)\/(.+\.mp4|avi)$' if regexp is None else regexp
    _regexp_video_dir = regexp[:regexp.rfind('\/')] + '$'  # Регулярка путь до папки с файлом
    _regexp_cam_dir = r'^(\/?.+)\/(\w+\-\d+)$'  # Регулярка путь до камеры на сервере

    # Выбрать необходимую регулярку в зависимости от пути
    regexp = regexp if re.match(regexp, video_path) is not None else _regexp_video_dir if re.match(
        _regexp_video_dir, video_path) is not None else _regexp_cam_dir

    # Если путь подходит под регулярные выражения
    if re.match(regexp, video_path) is not None:
        split_path_dict = re.findall(regexp, video_path)[0]
        return {
            'server': split_path_dict[0],
            'cam': split_path_dict[1] if len(split_path_dict) >= 2 else None,
            'video_path': split_path_dict[2] if len(split_path_dict) >= 3 else None,
            'video': split_path_dict[3] if len(split_path_dict) >= 4 else None
        }
    else:
        raise ValueError(f"Путь {video_path} - не соотвествует регулярному выражению")
