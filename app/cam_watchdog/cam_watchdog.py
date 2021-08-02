from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import logging

from time import sleep


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
            self.catch_all_handler(event)

        def on_created(self, event):
            self.catch_all_handler(event)

        def on_deleted(self, event):
            self.catch_all_handler(event)

        def on_modified(self, event):
            self.catch_all_handler(event)

    def start(self) -> None:
        """Запуск слежения за серверами"""
        self.cam_observer.start()
        while True:
            sleep(1)
