import sys
import pytest

from pathlib import Path

from app.video.ffmpeg import ffprobe

TEST_DIR_PATH = [path_ for path_ in sys.path if path_.endswith('test_video')][0]


def test_ffprobe_get_video_metadata():
    video_path = Path(TEST_DIR_PATH, 'files_for_test', 'test_video.mp4')

    video_metadata = ffprobe.get_video_metadata(video_path=video_path)

    assert 'streams' in video_metadata
    assert len(video_metadata.get('streams')) > 0
    for key in ['duration', 'bit_rate', 'codec_name']:
        assert key in video_metadata.get('streams')[0]


@pytest.mark.parametrize('invalid_path', [None, 'invalid'])
def test_ffprobe_get_invalid_video_metadata(invalid_path):
    with pytest.raises((FileNotFoundError, TypeError)):
        ffprobe.get_video_metadata(video_path=invalid_path)
