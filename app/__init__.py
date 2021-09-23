import sys
from pathlib import Path
from dotenv import load_dotenv
from app.logger import get_logger

log = get_logger("init_app")

_env_path = Path(sys.path[0], 'config.env')

if sys.version_info[0] < 3 or sys.version_info[1] < 8:
    log.error("Версия Python должна быть выше 3.8")
    sys.exit(1)

if _env_path.exists():
    load_dotenv(_env_path)
else:
    _env_path = Path('config.env')

    if _env_path.exists():
        load_dotenv(_env_path)
    else:
        log.error("Не обнаружен config.env! Выход..")
        sys.exit(1)
