"""Test configuration for SQHG's backend."""

import asyncio
from typing import Generator, AsyncGenerator

import pytest
import pytest_asyncio
from async_asgi_testclient import TestClient
from pytest import MonkeyPatch
from sqlalchemy.orm import Session

from main import app
from core.database import Database, engine, SessionLocal


@pytest.fixture(scope='session')
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()

    try:
        yield loop
    finally:
        loop.close()


@pytest.fixture(scope='function')
def database():
    connection = engine.connect()
    transaction = connection.begin()
    database = SessionLocal(bind=connection)

    try:
        yield database
    finally:
        database.close()
        transaction.rollback()
        connection.close()


@pytest_asyncio.fixture
async def client(database: Session, monkeypatch: MonkeyPatch) -> AsyncGenerator[TestClient, None]:
    app.dependency_overrides[Database] = lambda: database
    scope = {'client': ('0.0.0.0', '9000')}  # noqa: S104

    monkeypatch.setattr('sqlalchemy.orm.Session.query', database.query)

    async with TestClient(app, scope=scope) as client:
        yield client
