from datetime import datetime
from ast import literal_eval

from starlette import status
from app.web.api.filesystem import models, logic
from tests.mocks.consts import (
    MOCK_VIDEO_EXTENSION,
    MOCK_VIDEO_CODEC,
    MOCK_VIDEO_NAME,
    MOCK_VIDEO_PATH
)
from tests.mocks.database.video_server import *


def test_search_files(mock_get_server, mock_get_camera, mock_get_video_pool_by_datetime):
    payload = {
        "server": "api_test_server",
        "camera": "cam10",
        "datetime_start": datetime.strptime('03-08-2020 10:20:30', '%d-%m-%Y %H:%M:%S'),
        "datetime_end": datetime.strptime('03-08-2020 10:20:40', '%d-%m-%Y %H:%M:%S')
    }

    mock_get_server(server=payload.get("server"))
    mock_get_camera(server=payload.get("server"), camera=payload.get("camera"))
    mock_get_video_pool_by_datetime(camera=payload.get("camera"), video_datetime=payload.get("datetime_start"))

    response_result = logic.search_files(search_data=models.SearchFiles(**payload))

    assert response_result.status_code == status.HTTP_200_OK

    for key, value in literal_eval(response_result.body.decode()).items():
        assert (key, value) in {
            'id_server': len(payload.get("server")),
            'server': payload.get("server"),
            'cameras': [
                {
                    'id_camera': len(payload.get("camera")),
                    'camera': payload.get("camera"),
                    'videos': [
                        {
                            'id_video': int(payload.get('datetime_start').timestamp()),
                            'name': f'{MOCK_VIDEO_NAME}.{MOCK_VIDEO_EXTENSION}',
                            'path': f'{payload.get("server")}/{payload.get("camera")}/'
                                    f'{MOCK_VIDEO_PATH}/{MOCK_VIDEO_NAME}.{MOCK_VIDEO_EXTENSION}',
                            'record_date': str(payload.get("datetime_start")),
                            'duration': int(payload.get('datetime_start').timestamp()),
                            'bitrate': int(payload.get('datetime_start').timestamp()),
                            'codec': MOCK_VIDEO_CODEC
                        }
                    ]
                }
            ]
        }.items()


def test_search_files_incorrect_server():
    payload = {
        "server": "api_incorrect_test_server",
        "camera": '',
        "datetime_start": datetime.now(),
        "datetime_end": datetime.now()
    }

    response_result = logic.search_files(search_data=models.SearchFiles(**payload))

    assert response_result.status_code == status.HTTP_400_BAD_REQUEST
