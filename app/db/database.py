from peewee import MySQLDatabase, OperationalError
from app.utils.fpylog import Log
from .models import *

log = Log(file_log=True, file_log_name='db')


class Database:
    """Класс для работы с БД MySQL"""
    def __init__(self, user: str, password: str, host: str = 'localhost', database: str = 'video_server'):
        self.db = MySQLDatabase(
            user=user,
            password=password,
            host=host,
            database=database
        )

    def start(self) -> bool:
        """
        Создает подключение к БД, если не удается, то выводит ошибку о невозможности подключения
        Returns:
            bool: Состояние подключения к БД
        """
        try:
            self.db.connect()
            log.success(f"Подключение к бд успешно", log_file=False)
            return True
        except OperationalError as dbErr:
            log.error(dbErr)
            return False

    @staticmethod
    def _check_missing_tables(tables: list) -> list:
        """
        Проверяет недостающие таблицы, если такие есть, возвращает список недостающих моделей
        Args:
            tables(list): список моделей, которые необходимо проверить
        Returns:
            list: Вернет список недостающих моделей
        """
        missing_tables = [table for table in tables if not table.table_exists()]
        return missing_tables if missing_tables else False

    def _init_tables(self) -> None:
        """
        Инизиализирует таблицы БД
        Returns:
            None:
        """
        missing_tables = self._check_missing_tables([Cam, Video, VideoPath, VideoServer])

        if missing_tables:
            log.warn(f"Создание недостающих таблиц:")
            for table in missing_tables:
                print(table.__name__)

            try:
                self.db.create_tables(missing_tables)
                log.success("Таблицы успешно созданы")
            except OperationalError as dbErr:
                log.error(dbErr)

        else:
            log.success("Таблицы БД в порядке", log_file=False)

    async def init(self) -> bool:
        """
        Инициализирует базу данных
        Returns:
            bool: True - БД прошла инициализацию, False - не прошла
        """
        if self.start():
            self._init_tables()
            return True
        else:
            return False
