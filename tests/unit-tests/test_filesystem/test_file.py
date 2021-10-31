import sys
import pytest
import pathlib

from datetime import datetime

from app.filesystem import file


TEST_DIR_PATH = pathlib.Path(__file__).parent


def test_get_modification_date():
    payload_path = pathlib.Path(TEST_DIR_PATH, 'files_for_test', 'mod_test.file')
    creation_time = datetime.now()
    payload_path.touch()

    get_date = file.modification_date(payload_path)

    assert creation_time.hour == get_date.hour
    assert creation_time.minute == get_date.minute
    assert creation_time.second == get_date.second
