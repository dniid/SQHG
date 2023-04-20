"""SQLAlchemy database configuration for SQHG's backend."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from core.settings import (
    POSTGRES_USERNAME,
    POSTGRES_PASSWORD,
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_DATABASE
)


POSTGRES_URL = f'{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}'

engine = create_engine(f'postgresql+psycopg2://{POSTGRES_URL}')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
BaseModel = declarative_base()


async def Database():  # noqa: N802
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()
