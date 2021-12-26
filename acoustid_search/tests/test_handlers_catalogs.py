from typing import Any

from aiohttp.web import Application
from aiohttp.pytest_plugin import AiohttpClient


class MatchAnything:
    def __eq__(self, other: Any) -> bool:
        return True


async def test_catalog_get_ok(aiohttp_client: AiohttpClient, app: Application) -> None:
    client = await aiohttp_client(app)
    resp = await client.put("/main")
    assert resp.status == 200
    resp = await client.get("/main")
    assert resp.status == 200
    assert await resp.json() == {
        "catalog": "main",
        "status": {
            "created_at": MatchAnything(),
            "last_modified_at": MatchAnything(),
        },
    }


async def test_catalog_get_not_found(aiohttp_client: AiohttpClient, app: Application) -> None:
    client = await aiohttp_client(app)
    resp = await client.get("/main")
    assert resp.status == 404
    assert await resp.json() == {"error": {"type": "catalog_not_found"}}


async def test_catalog_put(aiohttp_client: AiohttpClient, app: Application) -> None:
    client = await aiohttp_client(app)
    resp = await client.put("/main")
    assert resp.status == 200
    assert await resp.json() == {"catalog": "main"}


async def test_catalog_patch(aiohttp_client: AiohttpClient, app: Application) -> None:
    client = await aiohttp_client(app)
    resp = await client.patch("/main")
    assert resp.status == 200
    assert await resp.json() == {"catalog": "main"}


async def test_catalog_delete(aiohttp_client: AiohttpClient, app: Application) -> None:
    client = await aiohttp_client(app)
    resp = await client.delete("/main")
    assert resp.status == 200
    assert await resp.json() == {}
