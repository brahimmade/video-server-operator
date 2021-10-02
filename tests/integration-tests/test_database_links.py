import sys
import pathlib
import pytest

from tests.common_fixtures import preload_database

from app.filesystem import database_links
from app.filesystem import path
from app.database import video_server


def test_link_full_path(preload_database):
    test_dir_path = [path_ for path_ in sys.path if path_.endswith('integration-tests')][0]
    payload_path = pathlib.Path(test_dir_path, 'test-files/cam-1/2021-05-05/123123/test_video.mp4')
    split_path = path.split_path(payload_path)

    database_links.set_full_path(video_path=payload_path)

    assert video_server.get_server(server_dir=split_path.get('server')) is not None
    assert video_server.get_camera(camera_dir=split_path.get('camera')) is not None
    assert video_server.get_video_path(video_path=split_path.get('video_path')) is not None
    assert video_server.get_video(name=split_path.get('video').replace('.mp4', '')) is not None


@pytest.mark.parametrize('invalid_path', [
    None,
    'incorrect',
    '/mnt/archive/test_server/cam-101/10-08-02/6580711/6580711-video.mp4'
])
def test_incorrect_link_full_path(preload_database, invalid_path):
    with pytest.raises(ValueError):
        database_links.set_full_path(video_path=invalid_path)
