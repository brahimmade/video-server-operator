import pytest
import pathlib

from datetime import datetime

from app.filesystem import path


def test_split_path():
    payload_path = pathlib.Path('/mnt/archive/test_server/cam-11/2021-08-02/6580713/6580713-video.mp4')

    split_path = path.split_path(path=payload_path)

    assert split_path == {
        'server': '/mnt/archive/test_server',
        'camera': 'cam-11',
        'video_date': '2021-08-02',
        'video_path': '6580713/6580713-video.mp4'
    }


@pytest.mark.parametrize('invalid_path', [None, 'incorrect'])
def test_split_incorrect_path(invalid_path):
    with pytest.raises(ValueError):
        path.split_path(path=invalid_path)


def test_find_datestamp():
    payload_path = '2021-08-02/6580713'

    datestamp = path.find_datestamp(path=payload_path)

    assert datestamp == datetime(year=2021, month=8, day=2)


@pytest.mark.parametrize('invalid_path', [None, 'incorrect'])
def test_find_incorrect_datestamp(invalid_path):
    assert path.find_datestamp(path=invalid_path) is None


def test_convert_to_pathlib():
    payload_path = 'test/convert/path'

    converted_path = path.convert_to_pathlib(payload_path)

    assert isinstance(converted_path, pathlib.Path)
    assert payload_path == converted_path.as_posix()


def test_convert_none_path():
    payload_path = None

    with pytest.raises(TypeError):
        path.convert_to_pathlib(payload_path)


def test_convert_non_existent_path():
    payload_path = 'test/convert/path'

    with pytest.raises(FileNotFoundError):
        path.convert_to_pathlib(path=payload_path, check_exist=True)