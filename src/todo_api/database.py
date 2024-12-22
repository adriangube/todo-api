from sqlalchemy import create_engine
from sqlalchemy.orm import Session, DeclarativeBase
from .settings import settings
engine = create_engine(settings.database_url)


class Base(DeclarativeBase):
    pass


def get_db_session():
    db_session = Session(bind=engine, autocommit=False, autoflush=False)
    try:
        yield db_session
    finally:
        db_session.close()
