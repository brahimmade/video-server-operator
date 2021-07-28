from app.utils.fpylog import Log

log = Log(file_log=False)


def exit_with_error_message(message: str) -> None:
    """
    Завершает программу с сообщением об ошибке
    """
    log.error(message)
    exit()
