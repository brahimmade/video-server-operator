import pytest
import asyncio

from app.database import video_server, BASE

__all__ = [
    'async_loop',
    'preload_database'
]


@pytest.fixture(scope='session')
def async_loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope="session")
def preload_database():
    """Предзагрузка базы данных, очистка, инициализация таблиц"""
    BASE.metadata.drop_all()
    video_server.init_tables()
    yield
