from watchdog.events import FileSystemEventHandler, FileMovedEvent, DirCreatedEvent, FileCreatedEvent
from watchdog.observers import Observer
from app.utils.fpylog import Log
from .file_logic import split_path
from asyncio import sleep as async_sleep


log = Log(file_log=True, file_log_name='watchdog')


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
                    print(video_split_dir)
                except ValueError as wdErr:
                    log.error(wdErr)

        def on_created(self, event):
            if isinstance(event, DirCreatedEvent):  # Если событие - создание новой папки
                try:
                    video_split_dir = split_path(event.src_path)
                    print(video_split_dir)
                except ValueError as wdErr:
                    log.error(wdErr)
            elif isinstance(event, FileCreatedEvent):  # Если событие - создание нового файла
                try:
                    video_split_dir = split_path(event.src_path)
                    print(video_split_dir)
                except ValueError as wdErr:
                    log.error(wdErr)

        def on_deleted(self, event):
            self.catch_all_handler(event)

        def on_modified(self, event):
            self.catch_all_handler(event)

    async def start(self) -> None:
        """Запуск слежения за серверами"""
        self.cam_observer.start()
        log.success(f"Запущен watchdog за директориями {self.cam_servers}", log_file=False)
        while True:
            await async_sleep(0.01)
