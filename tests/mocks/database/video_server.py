import pytest

from typing import AnyStr
from datetime import datetime

from app.database import video_server
from tests.mocks.consts import (
    MOCK_VIDEO_EXTENSION,
    MOCK_VIDEO_CODEC,
    MOCK_VIDEO_NAME,
    MOCK_VIDEO_PATH
)

__all__ = [
    'mock_get_server',
    'mock_get_video_pool_by_datetime',
    'mock_get_camera'
]


@pytest.fixture()
def mock_get_server(mocker):
    def mock(server: AnyStr):
        mocker.patch.object(video_server, 'get_server',
                            return_value=video_server.VideoServer(
                                id=len(server),
                                server_name=server,
                                server_dir=server
                            ))

    return mock


@pytest.fixture()
def mock_get_camera(mocker):
    def mock(camera: AnyStr, server: AnyStr):
        mocker.patch.object(video_server, 'get_camera',
                            return_value=video_server.Camera(
                                id=len(camera),
                                server_id=len(server),
                                camera_name=camera,
                                camera_dir=camera
                            ))

    return mock


@pytest.fixture()
def mock_get_video_pool_by_datetime(mocker):
    def mock(video_datetime: datetime, camera: AnyStr):
        mocker.patch.object(video_server, 'get_video_pool_by_datetime',
                            return_value=[video_server.Video(
                                id=int(video_datetime.timestamp()),
                                name=MOCK_VIDEO_NAME,
                                camera_id=len(camera),
                                video_path=MOCK_VIDEO_PATH,
                                record_date=video_datetime.date(),
                                record_time=video_datetime.time(),
                                extension=MOCK_VIDEO_EXTENSION,
                                duration=int(video_datetime.timestamp()),
                                bitrate=int(video_datetime.timestamp()),
                                codec=MOCK_VIDEO_CODEC
                            )])

    return mock
