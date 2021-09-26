from pathlib import Path
from watchdog.events import FileSystemEventHandler, FileMovedEvent, DirCreatedEvent, FileCreatedEvent
from watchdog.observers import Observer

from app.logger import get_logger
from app.filesystem import file_logic

log = get_logger(__name__)


class Watchdog:
    """Класс для слежения за состоянием директорий видео-серверов """

    def __init__(self, archives: list):
        """
        Args:
            archives (list of Path): Список путь до архивов с серверами
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

        @classmethod
        def catch_all_handler(cls, event):
            pass

        def on_moved(self, event) -> None:
            if isinstance(event, FileMovedEvent):  # Если событие - перемещение файла, а не директории
                try:
                    video_split_dir = file_logic.split_path(event.dest_path)
                except ValueError as err:
                    log.error(err)

        def on_created(self, event):
            # Если событие - создание новой папки
            if isinstance(event, DirCreatedEvent):
                try:
                    split_dir = file_logic.split_path(event.src_path)
                    if split_dir.get('server') is not None:
                        server = file_logic.set_server(split_dir.get('server'))

                        if split_dir.get('camera') is not None:
                            camera = file_logic.set_camera(camera_path=split_dir.get('camera'), server=server)

                            if split_dir.get('video_path') is not None:
                                video_path = file_logic.set_video_path(
                                    video_path=split_dir.get('video_path'),
                                    camera=camera)

                                if split_dir.get('video') is not None:
                                    pass
                                    # video = video_server.set_or_get_new_video(split_dir.get('video'))

                except ValueError as err:
                    log.error(err)

            # Если событие - создание нового файла
            elif isinstance(event, FileCreatedEvent):
                try:
                    pass
                    # video_split_dir = file_logic.split_path(event.src_path)
                except ValueError as err:
                    log.error(err)

        def on_deleted(self, event):
            self.catch_all_handler(event)

        def on_modified(self, event):
            log.info(event.src_path)
            self.catch_all_handler(event)

    def start(self) -> None:
        """Запуск слежения за архивами"""
        self.archive_observer.start()
        log.info(f"Запущен watchdog за директориями {self.archives}")
        # while True:
        #     await async_sleep(0.01)

    def stop(self) -> None:
        """Завершает слежение за архивами"""
        self.archive_observer.stop()
        log.info("Watchdog был остановлен")
