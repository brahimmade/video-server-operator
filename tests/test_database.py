import pytest
from datetime import datetime
from app.database import BASE, video_server


@pytest.fixture(name="preload_db", scope="session")
def preload_database():
    """Предзагрузка базы данных, очистка, инициализация таблиц"""
    BASE.metadata.drop_all()
    video_server.init_tables()
    yield


def test_set_video_server(preload_db):
    server_path = '/dev/archive/test_server'

    set_video_server = video_server.set_new_server(server_dir=server_path)

    assert isinstance(set_video_server, video_server.VideoServer)


def test_set_cam(preload_db):
    cam_path = 'cam1'
    set_video_server = video_server.set_new_server('/dev/archive/test_server')

    set_cam = video_server.set_new_camera(camera_dir=cam_path, server=set_video_server)

    assert isinstance(set_cam, video_server.Camera)


def test_set_video(preload_db):
    video_data = {
        'name': "test_video",
        'time': datetime.now().strftime('%H:%M:%S'),
        'extension': 'mp4',
        'duration': 10 * 60 * 60,
        'bitrate': 8340,
        'stream_count': 2,
        'codec_main': 'h264',
        'codec_sub': 'h264'
    }

    set_video = video_server.set_new_video(**video_data)

    assert isinstance(set_video, video_server.Video)


def test_set_incomplete_video(preload_db):
    video_data = {
        'name': "test_video_a",
        'time': datetime.now().strftime('%H:%M:%S'),
        'stream_count': 2,
        'codec_main': 'h264',
    }
    with pytest.raises(KeyError):
        video_server.set_new_video(**video_data)


def test_get_video_server(preload_db):
    server_path = '/dev/archive/test_server'
    set_video_server = video_server.set_new_server(server_dir=server_path)

    get_video_server = video_server.get_server_by_dir(server_dir=server_path)

    assert set_video_server == get_video_server
