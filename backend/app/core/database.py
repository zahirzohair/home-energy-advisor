from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool, QueuePool

from app.core.config import settings

_is_sqlite = settings.DATABASE_URL.startswith("sqlite")

_engine_kw: dict = {
    "echo": settings.DEBUG,
}
if _is_sqlite:
    _engine_kw["poolclass"] = NullPool
    _engine_kw["connect_args"] = {"check_same_thread": False}
else:
    _engine_kw["poolclass"] = QueuePool
    _engine_kw["pool_size"] = 10
    _engine_kw["max_overflow"] = 20
    _engine_kw["pool_pre_ping"] = True
    _engine_kw["pool_recycle"] = 3600

engine = create_engine(settings.DATABASE_URL, **_engine_kw)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, expire_on_commit=False
)
Base = declarative_base()


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_session():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
