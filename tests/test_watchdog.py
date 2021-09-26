import pytest
from time import sleep
from pathlib import Path
from shutil import rmtree
from app import filesystem
from app.database import video_server

WATCHDOG_TESTS_DIR = Path('watchdog_tests')


def create_path(path: Path) -> Path:
    if not path.exists():
        path.mkdir(parents=True)
    return path


@pytest.fixture(scope='session', autouse=True)
def start_watchdog():
    create_path(WATCHDOG_TESTS_DIR)
    wd = filesystem.Watchdog(archives=[WATCHDOG_TESTS_DIR])
    wd.start()
    yield
    rmtree(Path(WATCHDOG_TESTS_DIR))


def test_create_new_server(start_watchdog):
    server_path = Path(WATCHDOG_TESTS_DIR, 'TEST_SERVER')

    create_path(server_path)
    # Ожидание в 0.001 секунды, ибо работа watchdog происходит асинхронно,
    # В итоге проверка происходит раньше, чем выполняется работа
    sleep(0.001)
    assert video_server.get_server(server_dir=server_path) is not None


def test_create_new_camera(start_watchdog):
    camera_path = Path(WATCHDOG_TESTS_DIR, 'TEST_SERVER', 'cam-1')

    create_path(camera_path)

    sleep(0.001)
    assert video_server.get_camera(camera_dir=camera_path) is not None
