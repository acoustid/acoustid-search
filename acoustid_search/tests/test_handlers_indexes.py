from aiohttp.web import Application
from aiohttp.pytest_plugin import AiohttpClient


async def test_get_index(aiohttp_client: AiohttpClient, app: Application) -> None:
    client = await aiohttp_client(app)
    resp = await client.get("/main")
    assert resp.status == 200
    assert await resp.json() == {"index": "main"}


async def test_create_index(aiohttp_client: AiohttpClient, app: Application) -> None:
    client = await aiohttp_client(app)
    resp = await client.put("/main")
    assert resp.status == 200
    assert await resp.json() == {"index": "main"}


async def test_update_index(aiohttp_client: AiohttpClient, app: Application) -> None:
    client = await aiohttp_client(app)
    resp = await client.patch("/main")
    assert resp.status == 200
    assert await resp.json() == {"index": "main"}


async def test_delete_index(aiohttp_client: AiohttpClient, app: Application) -> None:
    client = await aiohttp_client(app)
    resp = await client.delete("/main")
    assert resp.status == 200
    assert await resp.json() == {}
