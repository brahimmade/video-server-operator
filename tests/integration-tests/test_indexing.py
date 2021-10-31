import pathlib

from app.filesystem import indexing
from app.database import video_server
from app.filesystem import path

TEST_DIR_PATH = pathlib.Path(__file__).parent


def test_indexing_unregister_files():
    payload_path = pathlib.Path(TEST_DIR_PATH, 'test-files', 'archive')
    test_files_paths = list(map(path.split_path, payload_path.rglob("*.[mM][pP]4")))

    indexing.indexing_unregister_files(archive_path=payload_path)

    for test_path in test_files_paths:
        server = video_server.get_server(server_dir=test_path.get("server"))
        assert server is not None

        camera = video_server.get_camera(server_id=server.id, camera_dir=test_path.get("camera"))
        assert camera is not None

        video = video_server.get_video(camera_id=camera.id, video_path=test_path.get("video_path"))
        assert video is not None


def test_indexing_absent_unregister_files():
    payload_path = pathlib.Path(TEST_DIR_PATH, 'test-files', 'wrong')

    indexing.indexing_unregister_files(archive_path=payload_path)
