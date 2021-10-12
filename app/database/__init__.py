from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy_utils import database_exists, create_database
from app.setting import MYSQL_URL


def create_session() -> scoped_session:
    """
    Создает сессию для подключения к базе данных
    Returns:
        scoped_session: Хранилище сессий
    """
    engine = create_engine(MYSQL_URL, pool_pre_ping=True)

    if not database_exists(engine.url):
        create_database(engine.url)

    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=BASE.metadata.bind, autoflush=False, expire_on_commit=False))


BASE = declarative_base()
SESSION = create_session()
