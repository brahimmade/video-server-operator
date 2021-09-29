import pytest

from datetime import datetime

from app.filesystem import file_logic


def test_split_path():
    payload_path = '/mnt/archive/test_server/cam-11/2021-08-02/6580713/6580713-video.mp4'

    split_path = file_logic.split_path(path=payload_path)

    assert split_path == {
        'server': '/mnt/archive/test_server',
        'camera': 'cam-11',
        'video_path': '2021-08-02/6580713',
        'video': '6580713-video.mp4'
    }


@pytest.mark.parametrize('invalid_path', [None, 'incorrect'])
def test_split_incorrect_path(invalid_path):
    with pytest.raises(ValueError):
        file_logic.split_path(path=invalid_path)


def test_find_datestamp():
    payload_path = '2021-08-02/6580713'

    datestamp = file_logic.find_datestamp(path=payload_path)

    assert datestamp == datetime(year=2021, month=8, day=2)


@pytest.mark.parametrize('invalid_path', [None, 'incorrect'])
def test_find_incorrect_datestamp(invalid_path):
    assert file_logic.find_datestamp(path=invalid_path) is None
