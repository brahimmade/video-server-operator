import sys
import time
import pytest
import shutil

from pathlib import Path
from app import filesystem
from app.database import video_server

TEST_DIR_PATH = [path_ for path_ in sys.path if path_.endswith('integration-tests')][0]
WATCHDOG_TESTS_DIR = Path(TEST_DIR_PATH, 'test-files', 'test_archive')


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
    shutil.rmtree(Path(WATCHDOG_TESTS_DIR))


def test_create_new_video(get_watchdog):
    test_video = Path(TEST_DIR_PATH, 'test-files/cam-1/2021-05-05/123123/test_video.mp4')
    video_path = Path(WATCHDOG_TESTS_DIR, 'test_server', 'cam-02', '2021-07-21', '6580114')
    create_path(video_path)
    video_file = Path(video_path, 'test_wd_video.mp4.tmp')
    shutil.copy(test_video, video_file)
    get_watchdog.start()

    video_file.replace(Path(video_path, 'test_wd_video.mp4'))

    # Сделать 10 попыток assert, так как watchdog работает в отдельном потоке
    # Поэтому тест не дожидается выполнения
    assertion_try = 0
    while assertion_try < 10:
        try:
            assert video_server.get_server(server_dir=Path(WATCHDOG_TESTS_DIR, 'test_server')) is not None
            assert video_server.get_camera(camera_dir=Path('cam-02')) is not None
            assert video_server.get_video(name='test_wd_video') is not None
            break
        except AssertionError as err:
            if assertion_try < 9:
                assertion_try += 1
                time.sleep(0.1)
            else:
                raise err
