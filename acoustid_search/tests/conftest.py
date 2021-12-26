import pytest
from aiohttp.web import Application
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from acoustid_search.app import create_app


async def create_tables(engine) -> None:
    from acoustid_search.db.schema import metadata

    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)


@pytest.fixture()
def db_engine(loop) -> AsyncEngine:
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        echo=False,
    )
    loop.run_until_complete(create_tables(engine))
    return engine


@pytest.fixture()
def app(loop, db_engine: AsyncEngine) -> Application:
    return create_app(db_engine)
