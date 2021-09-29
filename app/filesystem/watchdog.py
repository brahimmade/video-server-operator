from watchdog.events import FileSystemEventHandler, FileMovedEvent
from watchdog.observers import Observer

from app.logger import get_logger
from app.filesystem import database_links

log = get_logger(__name__)


class Watchdog:
    """Класс для слежения за состоянием файлов в архивах"""

    def __init__(self, archives: list):
        """
        Args:
            archives (list): Список путь до архивов с серверами
        """
        self.archives = [str(archive) for archive in archives]
        self.archive_observer = Observer()

        for archive in self.archives:
            self.archive_observer.schedule(self.ArchiveDirectoryHandling(), archive, recursive=True)

    class ArchiveDirectoryHandling(FileSystemEventHandler):
        """
        Наследуется от FileSystemEventHandler
        Обработчик ивентов изменений в директориях и файлах
        """

        def on_moved(self, event) -> None:
            """Обработчик событий перемещения"""
            if isinstance(event, FileMovedEvent):
                try:
                    database_links.set_full_path(event.dest_path)
                except ValueError as err:
                    log.error(err)

    def start(self) -> None:
        """Запуск слежения за архивами"""
        self.archive_observer.start()
        log.info(f"Запущен watchdog за директориями {self.archives}")

    def stop(self) -> None:
        """Завершает слежение за архивами"""
        self.archive_observer.stop()
        log.info("Watchdog был остановлен")
