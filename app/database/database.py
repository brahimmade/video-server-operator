from .models import *
from app.logger import get_logger


log = get_logger(__name__)


class Database:
    """Класс для работы с БД MySQL"""
    def __init__(self, user: str, password: str, host: str = 'localhost', database: str = 'video_server'):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.db = MySQLDatabase(
            user=self.user,
            password=self.password,
            host=self.host,
            database=self.database
        )
        self.models = [Cam, Video, VideoPath, VideoServer]

    def start(self) -> bool:
        """
        Создает подключение к БД, если не удается, то выводит ошибку о невозможности подключения
        Returns:
            bool: Состояние подключения к БД
        """
        try:
            self.db.connect()
            log.info(f"Подключение к бд успешно")
            return True
        except OperationalError as dbErr:
            log.error(dbErr)
            return False

    @classmethod
    def get_server_by_dir(cls, server_dir: str) -> VideoServer:
        """
        Вернет модель сервера по его директории
        Args:
            server_dir (str): Директория сервера

        Returns:
            app.db.models.VideoServer: Модель таблицы VideoServer
        """
        return VideoServer.get_or_create(server_dir=server_dir)[0]

    @classmethod
    def get_server_by_name(cls, server_name: str) -> VideoServer:
        """
        Вернет модель сервера по его названию
        Args:
            server_name (str): Название сервера

        Returns:
            app.db.models.VideoServer: Модель таблицы VideoServer
        """
        return VideoServer.get_or_create(server_name=server_name)[0]

    @classmethod
    def add_new_cam(cls, cam_dir: str, server: VideoServer) -> Cam:
        """
        Создать новую камеру в базе данных
        Args:
            cam_dir (str):
            server (app.db.models.VideoServer):

        Returns:
            app.db.models.Cam:
        Raises:
        """
        cam_model = Cam.create(
            server_id=server.id,
            cam_name=cam_dir,
            cam_dir=cam_dir
        )

        return cam_model

    @classmethod
    def _check_missing_tables(cls, tables: list) -> list:
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
        missing_tables = self._check_missing_tables(self.models)

        if missing_tables:
            log.info(f"Создание недостающих таблиц:")
            for table in missing_tables:
                print(table.__name__)

            try:
                self.db.create_tables(missing_tables)
                log.info("Таблицы успешно созданы")
            except OperationalError as dbErr:
                log.error(dbErr)

        else:
            log.info("Таблицы БД в порядке")

    def init(self):
        """
        Инициализирует базу данных
        Returns:
            None:
        """
        for _ in range(5):
            if self.start():
                self._init_tables()
                break

