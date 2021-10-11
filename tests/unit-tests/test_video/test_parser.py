import pytest
import sys

from datetime import datetime
from pathlib import Path

from app.video import parser

TEST_DIR_PATH = [path_ for path_ in sys.path if path_.endswith('test_video')][0]


def test_get_video_data():
    video_path = Path(TEST_DIR_PATH, 'files_for_test', 'test_video.mp4')
    reference_value = {
        'name': 'test_video',
        'extension': '.mp4',
        'record_time': datetime(2021, 10, 1, 16, 49, 8, 39728),
        'bitrate': '346368',
        'codec': 'h264',
        'duration': 0.5,
    }

    get_video_data = parser.get_video_data(video_path=video_path)

    assert get_video_data == reference_value


@pytest.mark.parametrize('invalid_path', [None, 'invalid'])
def test_get_video_data_with_incorrect_path(invalid_path):
    with pytest.raises((FileNotFoundError, TypeError)):
        parser.get_video_data(video_path=invalid_path)
