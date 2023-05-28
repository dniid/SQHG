"""SQLAlchemy database configuration for SQHG's backend."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from core.settings import (
    MYSQL_USERNAME,
    MYSQL_PASSWORD,
    MYSQL_HOST,
    MYSQL_PORT,
    MYSQL_DATABASE
)


MYSQL_URL = f'{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}'

engine = create_engine(f'mysql+pymysql://{MYSQL_URL}?charset=utf8mb4')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
BaseModel = declarative_base()


async def Database():  # noqa: N802
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()
