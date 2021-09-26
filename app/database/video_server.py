from datetime import datetime
from functools import total_ordering

from pathlib import Path
from sqlalchemy.sql import sqltypes, schema
from sqlalchemy.exc import SQLAlchemyError

from app.database import BASE, SESSION
from app.database.utils.decorators import with_insertion_lock
from app.database.utils.filters import leave_required_keys
from app.logger import get_logger

log = get_logger(__name__)


@total_ordering
class Video(BASE):
    """Модель таблицы с данными видеофайлов"""
    __tablename__ = 'video'
    id = schema.Column(sqltypes.Integer, primary_key=True)
    name = schema.Column(sqltypes.String(256), nullable=False)
    video_path_id = schema.Column(sqltypes.Integer,
                                  schema.ForeignKey('video_path.id', ondelete='CASCADE', onupdate='CASCADE'),
                                  nullable=False)
    time = schema.Column(sqltypes.Time(timezone=True), nullable=False)
    extension = schema.Column(sqltypes.String(6), nullable=False)
    duration = schema.Column(sqltypes.Integer, nullable=False)
    bitrate = schema.Column(sqltypes.Integer, nullable=False)
    stream_count = schema.Column(sqltypes.Integer, nullable=False)
    codec_main = schema.Column(sqltypes.String(10), nullable=False)
    codec_sub = schema.Column(sqltypes.String(10), nullable=True)

    def __repr__(self):
        return f"{self.id} | {self.name}.{self.extension} at {self.time} duration: {self.duration}"

    def __lt__(self, other):
        return self.id <= other.id

    def __eq__(self, other):
        return isinstance(other, Video) and self.id == other.id


@total_ordering
class VideoServer(BASE):
    """Модель таблицы Видео Сервера"""
    __tablename__ = 'video_server'
    id = schema.Column(sqltypes.Integer, primary_key=True)
    server_name = schema.Column(sqltypes.String(256), nullable=False)
    server_dir = schema.Column(sqltypes.String(256), nullable=False)

    def __repr__(self):
        return f"{self.id} | Server: {self.server_name} at {self.server_dir}"

    def __lt__(self, other):
        return self.id <= other.id

    def __eq__(self, other):
        return isinstance(other, VideoServer) and self.id == other.id


@total_ordering
class VideoPath(BASE):
    """ Модель таблицы с путями до директорий с видео"""
    __tablename__ = 'video_path'
    id = schema.Column(sqltypes.Integer, primary_key=True)
    camera_id = schema.Column(sqltypes.Integer,
                              schema.ForeignKey('camera.id', ondelete='CASCADE', onupdate='CASCADE'),
                              nullable=False)
    video_path = schema.Column(sqltypes.String(256), nullable=False)
    record_date = schema.Column(sqltypes.Date, nullable=False)

    def __repr__(self):
        return f"{self.id} | video: {self.video_id} for cam: {self.camera_id} at {self.record_date}"

    def __lt__(self, other):
        return self.id <= other.id

    def __eq__(self, other):
        return isinstance(other, VideoPath) and self.id == other.id


@total_ordering
class Camera(BASE):
    """Модель таблицы Камеры"""
    __tablename__ = 'camera'
    id = schema.Column(sqltypes.Integer, primary_key=True)
    server_id = schema.Column(sqltypes.Integer,
                              schema.ForeignKey('video_server.id', ondelete='CASCADE', onupdate='CASCADE'),
                              nullable=False)
    camera_name = schema.Column(sqltypes.String(16), nullable=False)
    camera_dir = schema.Column(sqltypes.String(256), nullable=False)

    def __repr__(self):
        return f"{self.id} | {self.camera_name} for server id: {self.server_id} at {self.camera_dir}"

    def __lt__(self, other):
        return self.id <= other.id

    def __eq__(self, other):
        return isinstance(other, Camera) and self.id == other.id


def init_tables():
    """Инициализация таблиц в базе данных"""
    VideoServer.__table__.create(checkfirst=True)
    Camera.__table__.create(checkfirst=True)
    VideoPath.__table__.create(checkfirst=True)
    Video.__table__.create(checkfirst=True)


@with_insertion_lock
def set_or_get_new_server(server_dir: str) -> VideoServer:
    """
    Создает новую запись с сервером
    Args:
        server_dir (str): Путь до папки сервера

    Returns:
        VideoServer: Модель с данными видео сервера
    """
    if server_dir is None:
        raise ValueError("Сервер не может быть NoneType")

    video_server = SESSION.query(VideoServer).filter_by(server_dir=server_dir).limit(1).scalar()
    if not video_server:
        video_server = VideoServer(
            server_name=server_dir[server_dir.rfind('/') + 1:],  # Найти / справа и отрезать все, что идет перед ним
            server_dir=server_dir)

        SESSION.add(video_server)
        try:
            SESSION.commit()
        except SQLAlchemyError as err:
            SESSION.rollback()
            raise ValueError from err
        finally:
            SESSION.close()

    return video_server


@with_insertion_lock
def set_or_get_new_camera(camera_dir: str, server: VideoServer) -> Camera:
    """
    Добавляет новую камеру в базу данных
    Args:
        camera_dir (str): Путь до камеры
        server (app.db.models.VideoServer): Модель таблицы Видео Сервера,
                                            для которой необходимо добавить камеру

    Returns:
        Camera: Модель с данными камеры
    """
    camera = SESSION.query(Camera).filter_by(camera_dir=camera_dir).limit(1).scalar()
    if not camera:
        camera = Camera(
            server_id=server.id,
            camera_name=camera_dir,
            camera_dir=camera_dir)

        SESSION.add(camera)
        SESSION.commit()

    SESSION.close()
    return camera


@with_insertion_lock
def set_or_get_new_video(**kwargs) -> Video:
    """
    Добавляет новое видео в базу данных
    Args:
        **kwargs: Аргументы с данными о видео
    Keyword Args:
        name (str): Название видео
        video_path_id (id): ID записи video_path для этой камеры
        time (str): Временая метка, с которого идет запись
        extension (str): Расширение видео файла
        duration (int): Длина видеоряда
        bitrate (int): Битрейт видеоряда
        stream_count (int): Количество потоков
        codec_main (str): Кодек главного потока
        codec_sub (str): Кодек второго потока
    Returns:
        Camera: Модель с данными видео

    Raises:
        KeyError: Если были переданны не все необходимые поля
    """
    # Удаляем неуказанные kwargs
    required_fields = Video.__table__.columns.keys()
    filtered_kwargs = leave_required_keys(kwargs, required_fields)
    required_fields.remove('id')  # Убираем поле id из требуемых, так как оно авто-инкриминирующее
    required_fields.remove('codec_sub')  # Убираем поле codec_sub из требуемых, так как оно не обязательно
    # Проверка того, что все необходимые поля переданы
    if set(required_fields) - set(filtered_kwargs):
        raise KeyError('Не были переданы все необходимые поля')

    if filtered_kwargs.get('stream_count') > 1 and filtered_kwargs is None:
        log.warning("Количество потоков больше 1, но кодек дополнительного потока не был указан. "
                    "Будет задан основной кодек!")

    video = SESSION.query(Video).filter_by(**filtered_kwargs).limit(1).scalar()
    if not video:
        video = Video(**filtered_kwargs)
        SESSION.add(video)
        SESSION.commit()

    SESSION.close()
    return video


@with_insertion_lock
def set_or_get_new_video_path(camera: Camera, video_path: [str, Path], datestamp: datetime) -> Camera:
    """
    Добавляет новую камеру в базу данных
    Args:
        camera (Camera): Модель таблицы Камеры, для которой указывается путь до видео
        video_path (str | Path): Путь до видео
        datestamp (datetime): Дата, когда было записано видео

    Returns:
        Camera: Модель с данными камеры
    """
    set_video_path = SESSION.query(VideoPath).filter_by(
        camera_id=camera.id,
        video_path=video_path,
        record_date=datestamp).limit(1).scalar()

    if not set_video_path:
        set_video_path = VideoPath(
            camera_id=camera.id,
            video_path=video_path,
            record_date=datestamp
        )
        SESSION.add(set_video_path)
        SESSION.commit()

    SESSION.close()
    return set_video_path


def get_server(**kwargs) -> [VideoServer, None]:
    """
    Получить модель видео сервера по заданным параметрам
    Args:
        **kwargs: Данные модели сервера

    Keyword Args:
        id (int): ID записи в таблице
        server_name (str): Название сервера
        server_dir (str | Path): Путь до сервера

    Returns:
        VideoServer: Модель с данными о сервере
        None: Если по переданным параметрам не было найдено сервера
    """
    filtered_fields = leave_required_keys(kwargs, VideoServer.__table__.columns.keys())

    if 'server_dir' in filtered_fields.keys():
        filtered_fields['server_dir'] = str(filtered_fields.get('server_dir')).replace("\\", '/')

    video_server = SESSION.query(VideoServer).filter_by(**filtered_fields).limit(1).scalar()
    SESSION.close()
    return video_server


def get_camera(**kwargs) -> [Camera, None]:
    """
    Получить модель камеры по заданным параметрам
    Args:
        **kwargs: Данные модели камеры

    Keyword Args:
        id (int): ID записи в таблице
        server_id (int): ID сервера, к которому привязанна камера
        camera_name (str): Название камеры
        camera_dir (str | Path): Путь до камеры

    Returns:
        Camera: Модель с данными о камере
        None: Если по переданным параметрам не было найдено камер
    """
    filtered_fields = leave_required_keys(kwargs, Camera.__table__.columns.keys())

    if 'camera_dir' in filtered_fields.keys():
        filtered_fields['camera_dir'] = str(filtered_fields.get('camera_dir')).replace("\\", '/')

    camera = SESSION.query(Camera).filter_by(**filtered_fields).limit(1).scalar()
    SESSION.close()
    return camera


if __name__ != '__main__':
    init_tables()
