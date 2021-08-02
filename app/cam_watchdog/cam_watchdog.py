from watchdog.events import FileSystemEventHandler, FileMovedEvent
from watchdog.observers import Observer
from app.utils.fpylog import Log
from .file_logic import CamVideoPath
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
        def catch_all_handler(self, event):
            print(event)

        def on_moved(self, event):
            if isinstance(event, FileMovedEvent):
                video = CamVideoPath(path_video=event.dest_path.replace('\\', '/'))
                try:
                    video.split_for_tables()
                except ValueError as wdErr:
                    log.error(wdErr)

        def on_created(self, event):
            self.catch_all_handler(event)

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
