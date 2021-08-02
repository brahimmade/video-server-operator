import peewee
from dotenv import get_key as env_get_key
from app.setting import DOT_ENV_PATH


class BaseModel(peewee.Model):
    """Базовый класс для моделей с бд MySQL"""
    id = peewee.PrimaryKeyField(null=False)

    class Meta:
        # Ниже представлен небольшой костыль, ибо записывание переменных из config.env в переменные среды
        # происходит позже, чем инициализация пакетов и этих моделей. Следовательно, сюда передавались None..
        database = peewee.MySQLDatabase(user=env_get_key(DOT_ENV_PATH, 'DB_USER'),
                                        password=env_get_key(DOT_ENV_PATH, 'DB_PASSWORD'),
                                        database=env_get_key(DOT_ENV_PATH, 'DB_NAME'),
                                        host=env_get_key(DOT_ENV_PATH, 'DB_HOST'))


class VideoServer(BaseModel):
    """Модель таблицы Видео Сервера"""
    server_name = peewee.CharField(null=False, verbose_name="Название сервера")
    server_dir = peewee.CharField(max_length=256, null=False, verbose_name='Директория сервера')


class Cam(BaseModel):
    """Модель таблицы Камеры"""
    server_id = peewee.ForeignKeyField(model=VideoServer, to_field='id', on_delete='cascade', on_update='cascade',
                                       verbose_name='ID сервера')
    cam_name = peewee.CharField(null=False, verbose_name="Название камеры")
    cam_dir = peewee.CharField(max_length=256, null=False, verbose_name='Директория камеры')


class Video(BaseModel):
    """Модель таблицы с путями до видеофайлов """
    name = peewee.CharField(max_length=256, null=False, verbose_name="Название видео")
    time = peewee.TimeField(formats=['HH:mm:ss'], null=False, verbose_name="Время записи")
    extension = peewee.CharField(max_length=6, null=False, verbose_name="Расширение")
    duration = peewee.IntegerField(default=0, null=False, verbose_name="Длина видео")
    bitrate = peewee.IntegerField(null=False, verbose_name="Битрейт")
    stream_count = peewee.IntegerField(null=False, verbose_name="Количество потоков")
    codec_main = peewee.CharField(max_length=10, null=False, verbose_name="Кодек главного потока")
    codec_sub = peewee.CharField(max_length=10, null=True, verbose_name="Кодек дополнительного потока")


class VideoPath(BaseModel):
    """ Модель таблицы с путями до директорий с видео"""
    cam_id = peewee.ForeignKeyField(model=VideoServer, to_field='id', on_delete='cascade', on_update='cascade',
                                    verbose_name='ID Камеры')
    video_id = peewee.ForeignKeyField(model=Video, to_field='id', on_delete='cascade', on_update='cascade',
                                      verbose_name='ID Видео')
    record_date = peewee.DateField(formats=['YYYY-MM-dd'], null=False, verbose_name="Дата записи")
