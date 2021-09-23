from sqlalchemy.sql import sqltypes, schema
from app.database import BASE, SESSION
from app.database.utils.decorators import with_insertion_lock


class Video(BASE):
    """Модель таблицы с путями до видеофайлов """
    __tablename__ = 'video'
    id = schema.Column(sqltypes.Integer, primary_key=True)
    name = schema.Column(sqltypes.String(256), nullable=False)
    time = schema.Column(sqltypes.Time(timezone=True), nullable=False)
    extension = schema.Column(sqltypes.String(6), nullable=False)
    duration = schema.Column(sqltypes.Integer, nullable=False)
    bitrate = schema.Column(sqltypes.Integer, nullable=False)
    stream_count = schema.Column(sqltypes.Integer, nullable=False)
    codec_main = schema.Column(sqltypes.String(10), nullable=False)
    codec_sub = schema.Column(sqltypes.String(10), nullable=True)

    def __repr__(self):
        return f"{self.id} | {self.name}.{self.ext} at {self.time} duration: {self.duration}"


class VideoServer(BASE):
    """Модель таблицы Видео Сервера"""
    __tablename__ = 'video_server'
    id = schema.Column(sqltypes.Integer, primary_key=True)
    server_name = schema.Column(sqltypes.String(256), nullable=False)
    server_dir = schema.Column(sqltypes.String(256), nullable=False)


class VideoPath(BASE):
    """ Модель таблицы с путями до директорий с видео"""
    __tablename__ = 'video_path'
    id = schema.Column(sqltypes.Integer, primary_key=True)
    cam_id = schema.Column(sqltypes.Integer,
                           schema.ForeignKey('cam.id', ondelete='CASCADE', onupdate='CASCADE'),
                           nullable=False)
    video_id = schema.Column(sqltypes.Integer,
                             schema.ForeignKey('video.id', ondelete='CASCADE', onupdate='CASCADE'),
                             nullable=False)
    record_date = schema.Column(sqltypes.Date, nullable=False)

    def __repr__(self):
        return f"{self.id} | video: {self.video_id} for cam: {self.cam_id} at {self.record_date}"


class Cam(BASE):
    """Модель таблицы Камеры"""
    __tablename__ = 'cam'
    id = schema.Column(sqltypes.Integer, primary_key=True)
    server_id = schema.Column(sqltypes.Integer,
                              schema.ForeignKey('video_server.id', ondelete='CASCADE', onupdate='CASCADE'),
                              nullable=False)
    cam_name = schema.Column(sqltypes.String(16), nullable=False)
    cam_dir = schema.Column(sqltypes.String(256), nullable=False)


def init_tables():
    """Инициализация таблиц в базе данных"""
    VideoServer.__table__.create(checkfirst=True)
    Cam.__table__.create(checkfirst=True)
    Video.__table__.create(checkfirst=True)
    VideoPath.__table__.create(checkfirst=True)


@with_insertion_lock
def add_new_server(server_dir: str) -> VideoServer:
    """
    Создает новую запись с сервером
    Args:
        server_dir (str): Путь до папки сервера

    Returns:
        VideoServer: Модель VideoServer
    """
    video_server = SESSION.query(VideoServer).filter(VideoServer.server_dir == server_dir).limit(1).scalar()
    if not video_server:
        video_server = VideoServer(
            server_name=server_dir[server_dir.rfind('/') + 1:],  # Найти / справа и отрезать все, что идет перед ним
            server_dir=server_dir)

        SESSION.add(video_server)
        SESSION.commit()
    return video_server


if __name__ != '__main__':
    init_tables()
