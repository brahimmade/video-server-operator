from starlette import status
from starlette.responses import JSONResponse

from app.database import video_server
from .models import SearchFiles


def search_files(search_data: SearchFiles) -> JSONResponse:
    """
    Поиск видео файлов в базе данных по переданным параметрам
    Args:
        search_data (SearchFiles): Модель параметров запроса SearchFiles

    Returns:
        JSONResponse: Ответ в формате JSON с полными данными по запрашиваемым файлам

    """

    server_data = video_server.get_server(**{'id': search_data.server} if isinstance(search_data.server, int) else {
        'server_name': search_data.server})

    response = JSONResponse

    if server_data is None or not isinstance(server_data, video_server.VideoServer):
        response = response(content={"message": f"Server {search_data.server} - does not exist"},
                            status_code=status.HTTP_400_BAD_REQUEST)
    else:
        camera_list = [video_server.get_camera(
            server_id=server_data.id,
            **{'id': camera} if isinstance(camera, int) else {'camera_name': camera})
            for camera in (search_data.camera if isinstance(search_data.camera, list) else [search_data.camera])]

        camera_list = [{
            **camera.__dict__,
            'videos': video_server.get_video_pool_by_datetime(time_start=search_data.datetime_start,
                                                              time_end=search_data.datetime_end,
                                                              camera=camera)
        } for camera in camera_list if camera is not None]

        content = {
            'id_server': server_data.id,
            'server': server_data.server_name,
            'cameras': [
                {
                    'id_camera': camera.get('id'),
                    'camera': camera.get('camera_name'),
                    'videos': [
                        {
                            'id_video': video.id,
                            'name': f"{video.name}.{video.extension}",
                            'path': f"{server_data.server_dir}/{camera.get('camera_dir')}/"
                                    f"{video.video_path}/{video.name}.{video.extension}",
                            'record_date': f"{video.record_date} {video.record_time}",
                            'duration': video.duration,
                            'bitrate': video.bitrate,
                            'codec': video.codec
                        } for video in camera.get('videos')
                    ]
                } for camera in camera_list
            ]
        } if server_data is not None else {'message': f"{search_data.server} - does not exist"}

        response = response(content=content, status_code=status.HTTP_200_OK)

    return response
