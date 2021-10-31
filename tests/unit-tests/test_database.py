import pytest

from datetime import datetime
from random import randint

from app.database import video_server

from tests.common_fixtures import preload_database
from tests.utils.generators import random_string
from tests.mocks.consts import MOCK_VIDEO_CODEC, MOCK_VIDEO_EXTENSION


@pytest.fixture()
def set_testing_server():
    def set_server(server_path: str = f'/dev/archive/{random_string(10)}') -> video_server.VideoServer:
        return video_server.set_or_get_new_server(server_path)

    return set_server


@pytest.fixture()
def set_testing_camera(set_testing_server):
    def set_camera(camera_name: str = f'cam{randint(100, 999)}',
                   server: video_server.VideoServer = set_testing_server()) -> video_server.Camera:
        return video_server.set_or_get_new_camera(camera_dir=camera_name, server=server)

    return set_camera


@pytest.fixture()
def set_testing_video(set_testing_camera):
    def set_video(camera: video_server.Camera = set_testing_camera()) -> video_server.Video:
        video_data = {
            'name': random_string(8),
            'video_path': f"{randint(1, 30)}-{randint(1, 12)}-2021/62241721",
            'camera_id': camera.id,
            'record_date': datetime.now().date(),
            'record_time': datetime.now().time(),
            'extension': MOCK_VIDEO_EXTENSION,
            'duration': 10 * 60 * 60,
            'bitrate': 8340,
            'codec': MOCK_VIDEO_CODEC,
        }
        return video_server.set_or_get_new_video(**video_data)

    return set_video


def test_set_video_server(set_testing_server):
    set_video_server = set_testing_server()

    assert isinstance(set_video_server, video_server.VideoServer)


@pytest.mark.parametrize('invalid_server', [None, 'long' * 65])
def test_set_invalid_video_server(invalid_server):
    with pytest.raises(ValueError):
        video_server.set_or_get_new_server(invalid_server)


def test_set_cam(set_testing_camera):
    set_cam = set_testing_camera()

    assert isinstance(set_cam, video_server.Camera)


def test_set_video(set_testing_video):
    set_video = set_testing_video()

    assert isinstance(set_video, video_server.Video)


def test_set_incomplete_video():
    with pytest.raises(KeyError):
        video_server.set_or_get_new_video(**{})


def test_get_video_server(set_testing_server):
    set_video_server = set_testing_server()

    get_video_server = video_server.get_server(server_dir=set_video_server.server_dir)

    assert set_video_server == get_video_server


def test_get_camera(set_testing_camera):
    set_camera = set_testing_camera()

    get_camera = video_server.get_camera(camera_dir=set_camera.camera_dir)

    assert set_camera == get_camera


def test_video_pool_by_date(set_testing_video, set_testing_camera):
    testing_camera = set_testing_camera()
    first_video = set_testing_video(camera=testing_camera)
    second_video = set_testing_video(camera=testing_camera)

    get_video_pool = video_server.get_video_pool_by_datetime(
        time_start=datetime.combine(date=first_video.record_date, time=first_video.record_time),
        time_end=datetime.combine(date=second_video.record_date, time=second_video.record_time),
        camera=testing_camera)

    assert get_video_pool == [first_video, second_video]


def test_video_pool_by_incorrect_date(set_testing_camera):
    set_camera = set_testing_camera()
    empty_video_list = video_server.get_video_pool_by_datetime(time_start=datetime.max,
                                                               time_end=datetime.max,
                                                               camera=set_camera)
    assert not empty_video_list


def test_get_all_servers(set_testing_server):
    set_video_server = set_testing_server()

    get_all_video_servers = video_server.get_all_video_servers()

    assert set_video_server in get_all_video_servers


def test_get_all_cameras(set_testing_server, set_testing_camera):
    set_video_server = set_testing_server()
    set_camera = set_testing_camera(server=set_video_server)

    get_all_cameras = video_server.get_all_cameras_at_server(server=set_video_server)

    assert set_camera in get_all_cameras


def test_get_all_cameras_from_non_existent_server():
    get_camera = video_server.get_all_cameras_at_server(server=video_server.VideoServer())

    assert not len(get_camera)


def test_get_all_video_from_camera(set_testing_camera, set_testing_video):
    set_camera = set_testing_camera()
    set_video = set_testing_video()

    get_all_video = video_server.get_all_videos_from_camera(camera=set_camera)

    assert set_video in get_all_video


def test_get_all_video_from_non_existent_camera():
    get_video = video_server.get_all_videos_from_camera(camera=video_server.Camera())

    assert not len(get_video)
