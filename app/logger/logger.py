import logging
from pathlib import Path


def get_logger(name: str, log_level: str = 'INFO') -> logging.Logger:
    """
    Получить сконфигурированный логгер
    Args:
        name (str): Название модуля
        log_level (str): Уровень лога

    Returns:
        logging.Logger: Сконфигурированный экземпляр логгера
    """
    log_format = "%(asctime)s [%(levelname)s] - %(name)s | %(message)s"
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)
    stream_handler.setFormatter(logging.Formatter(log_format))

    log_path = Path('logs')
    if not log_path.exists():
        log_path.mkdir(parents=True)

    log_file = Path(log_path, 'vso.log')
    if not log_file.exists():
        log_file.touch()

    file_handler = logging.FileHandler(
        filename=log_file,
        encoding='utf-8')
    file_handler.setLevel(log_level)
    file_handler.setFormatter(logging.Formatter(log_format))

    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    return logger
