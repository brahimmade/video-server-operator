import pathlib

from app.database import video_server
from app.filesystem import path
from app.video import parser


def set_full_path(video_path: [str, pathlib.Path]) -> None:
    """
    Отправить все данные пути в базу данных
    Args:
        video_path (str | pathlib.Path): Путь до видео
    Raises:
        ValueError: Ошибка возникает, если переданный путь оказался некорректным
    """
    try:
        parsed_path = path.split_path(video_path)

        video_datestamp = path.find_datestamp(parsed_path.get('video_path'))
        # Проверка, если поиск даты вернул None
        if video_datestamp is None:
            raise ValueError("В переданном пути video_path не была найдена дата")

        set_server = video_server.set_or_get_new_server(server_dir=parsed_path.get('server'))
        set_camera = video_server.set_or_get_new_camera(camera_dir=parsed_path.get('camera'),
                                                        server=set_server)
        video_server.set_or_get_new_video(**parser.get_video_data(video_path=video_path),
                                          camera_id=set_camera.id,
                                          video_path=parsed_path.get('video_path'),
                                          record_date=video_datestamp)
    except ValueError as err:
        raise err
