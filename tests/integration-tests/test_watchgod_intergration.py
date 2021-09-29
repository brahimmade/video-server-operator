import time
import pytest
from pathlib import Path
from shutil import rmtree
from app import filesystem
from app.database import video_server

WATCHDOG_TESTS_DIR = Path('watchdog_tests')


def create_path(path: Path) -> Path:
    if not path.exists():
        path.mkdir(parents=True)
    return path


@pytest.fixture(scope='session')
def get_watchdog():
    create_path(WATCHDOG_TESTS_DIR)
    wd = filesystem.Watchdog(archives=[WATCHDOG_TESTS_DIR])
    yield wd
    wd.stop()
    rmtree(Path(WATCHDOG_TESTS_DIR))


def test_create_new_video(get_watchdog):
    video_path = Path(WATCHDOG_TESTS_DIR, 'test_server', 'cam-02', '2021-07-21', '6580114')
    create_path(video_path)
    video_file = Path(video_path, 'test.mp4.tmp')
    video_file.touch()
    get_watchdog.start()
    video_file.replace(Path(video_path, 'test.mp4'))

    # Сделать 10 попыток assert, так как watchdog работает в отдельном потоке
    # Поэтому тест не дожидается выполнения
    assertion_try = 0
    while assertion_try < 10:
        try:
            assert video_server.get_server(server_dir=Path(WATCHDOG_TESTS_DIR, 'test_server')) is not None
            break
        except AssertionError:
            if assertion_try < 10:
                assertion_try += 1
                time.sleep(0.1)
            else:
                raise
