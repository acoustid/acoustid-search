import pytest
from aiohttp.web import Application
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from acoustid_search.app import create_app
from acoustid_search.index import IndexClient
from acoustid_search.backend import BackendRegistry
from acoustid_search.legacy.backend import LegacySearchBackend


async def create_tables(engine) -> None:
    from acoustid_search.db.schema import metadata

    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)


async def create_legacy_tables(engine) -> None:
    from acoustid_search.legacy.db.schema import metadata

    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)


@pytest.fixture()
def legacy_db(loop) -> AsyncEngine:
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        echo=False,
    )
    loop.run_until_complete(create_legacy_tables(engine))
    return engine


@pytest.fixture()
def app(loop, legacy_db: AsyncEngine) -> Application:
    backends = BackendRegistry()
    backends.register_backend("legacy", LegacySearchBackend(legacy_db, IndexClient('http://localhost:6081'), "acoustid"))
    backends.route("acoustid", "legacy")
    return create_app(backends)
