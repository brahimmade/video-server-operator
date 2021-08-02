from re import findall as re_findall


class CamVideoPath:
    def __init__(self, path_video: str):
        self.video_path = path_video

    def split_for_tables(self, regexp: str = None) -> dict:
        """
        Разделяет строку на директории для базы данныъх
        Args:
            regexp (str): Кастомное регулярное выражение для поиска путей

        Returns:
            dict: Возвращает словарь с ключами для баз данных 'server, 'cam', 'video', 'video_path

        Raises:
            ValueError: Вернет ошибку, если путь не соответсвует регулярному выражению

        """
        regexp = r'^(\/?.+)\/(.+\d+)\/(\d{4}\-\d{2}\-\d{2}\/.+)\/(.+\.mp4|avi)$' if regexp is None else regexp
        split_path = re_findall(regexp, self.video_path)[0]
        if split_path:
            return {
                'server': split_path[0],
                'cam': split_path[1],
                'video_path': split_path[2],
                'video': split_path[3]
            }
        else:
            raise ValueError(f"Путь {self.video_path} - не соотвествует регулярному выражению")
