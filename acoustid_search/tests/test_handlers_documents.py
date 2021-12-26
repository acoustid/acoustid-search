from aiohttp.web import Application
from aiohttp.pytest_plugin import AiohttpClient


async def test_get_document(aiohttp_client: AiohttpClient, app: Application) -> None:
    client = await aiohttp_client(app)
    resp = await client.get("/main/_doc/1")
    assert resp.status == 200
    assert await resp.json() == {"index": "main", "id": "1"}


async def test_create_document(aiohttp_client: AiohttpClient, app: Application) -> None:
    client = await aiohttp_client(app)
    resp = await client.put("/main/_doc/1")
    assert resp.status == 200
    assert await resp.json() == {"index": "main", "id": "1"}


async def test_delete_document(aiohttp_client: AiohttpClient, app: Application) -> None:
    client = await aiohttp_client(app)
    resp = await client.delete("/main/_doc/1")
    assert resp.status == 200
    assert await resp.json() == {"index": "main", "id": "1"}
