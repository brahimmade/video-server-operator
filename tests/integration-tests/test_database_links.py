import pytest

from tests.common_fixtures import preload_database

from app.filesystem import database_links
from app.filesystem import file_logic
from app.database import video_server


def test_link_full_path(preload_database):
    payload_path = '/mnt/archive/test_server/cam-101/2023-08-02/6580711/6580711-video.mp4'
    split_path = file_logic.split_path(payload_path)

    database_links.set_full_path(video_path=payload_path)

    assert video_server.get_server(server_dir=split_path.get('server')) is not None
    assert video_server.get_camera(camera_dir=split_path.get('camera')) is not None
    assert video_server.get_video_path(video_path=split_path.get('video_path')) is not None
    # assert video_server.get_video(name=split_path.get('video')) is not None


@pytest.mark.parametrize('invalid_path', [
    None,
    'incorrect',
    '/mnt/archive/test_server/cam-101/10-08-02/6580711/6580711-video.mp4'
])
def test_incorrect_link_full_path(preload_database, invalid_path):
    with pytest.raises(ValueError):
        database_links.set_full_path(video_path=invalid_path)
