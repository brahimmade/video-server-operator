from watchdog.events import FileSystemEventHandler, FileMovedEvent, DirCreatedEvent, FileCreatedEvent
from watchdog.observers import Observer
from .file_logic import split_path
from asyncio import sleep as async_sleep
from app.logger import get_logger
from app.database import video_server

log = get_logger(__name__)


class CamWatchdog:
    """Класс для слежения за состоянием директорий видео-серверов """

    def __init__(self, cam_servers: list):
        self.cam_servers = cam_servers
        self.cam_observer = Observer()

        for server in self.cam_servers:
            self.cam_observer.schedule(self.CamDirectoryHandling(), server, recursive=True)

    class CamDirectoryHandling(FileSystemEventHandler):
        """
        Наследуется от FileSystemEventHandler
        Обработчик ивентов изменений в директориях и файлах
        """

        def catch_all_handler(self, event):
            pass

        def on_moved(self, event) -> None:
            if isinstance(event, FileMovedEvent):  # Если событие - перемещение файла, а не директории
                try:
                    video_split_dir = split_path(event.dest_path)
                except ValueError as err:
                    log.error(err)

        def on_created(self, event):
            # Если событие - создание новой папки
            if isinstance(event, DirCreatedEvent):
                try:
                    video_split_dir = split_path(event.src_path)
                    server_model = video_server.get_server_by_dir(video_split_dir.get('server'))
                    video_server.set_new_camera(camera_dir=video_split_dir.get('cam'), server=server_model)

                except ValueError as err:
                    log.error(err)

            # Если событие - создание нового файла
            elif isinstance(event, FileCreatedEvent):
                try:
                    video_split_dir = split_path(event.src_path)
                except ValueError as err:
                    log.error(err)

        def on_deleted(self, event):
            self.catch_all_handler(event)

        def on_modified(self, event):
            self.catch_all_handler(event)

    async def start(self) -> None:
        """Запуск слежения за серверами"""
        self.cam_observer.start()
        log.info(f"Запущен watchdog за директориями {self.cam_servers}")
        while True:
            await async_sleep(0.01)
