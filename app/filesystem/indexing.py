from os import PathLike, cpu_count
from typing import AnyStr
from concurrent.futures import ThreadPoolExecutor

from pathlib import Path

from app.filesystem import database_links
from app.logger import get_logger


log = get_logger(__name__)


def indexing_unregister_files(archive_path: [PathLike, AnyStr]) -> None:
    """
    Индексирование видеофайлов в директориях архивов
    Args:
        archive_path (PathLike, AnyStr): Путь до архивов
    """
    log.info("Start indexing video file, please, wait")
    with ThreadPoolExecutor(cpu_count() or 1) as thread_executor:
        thread_executor.map(database_links.set_full_path, list(Path(archive_path).rglob("*.[mM][pP]4")))
    log.info("Indexing successful!")
