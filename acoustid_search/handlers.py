import datetime

from aiohttp import web
from sqlalchemy.ext.asyncio import AsyncEngine as DatabaseEngine

from acoustid_search.db.operations import get_catalog, create_catalog, delete_catalog

routes = web.RouteTableDef()


def get_db_engine(request: web.Request) -> DatabaseEngine:
    return request.app["db"]


@routes.get("/{catalog}")
async def handle_catalog_get(request: web.Request) -> web.Response:
    catalog_name = request.match_info["catalog"]
    async with get_db_engine(request).begin() as db:
        catalog = await get_catalog(db, catalog_name)
        if catalog is None:
            return web.json_response({"error": {"type": "catalog_not_found"}}, status=404)
        return web.json_response(
            {
                "catalog": catalog_name,
                "status": {
                    "created_at": catalog.created_at.astimezone(datetime.timezone.utc).isoformat(),
                    "last_modified_at": catalog.last_modified_at.astimezone(datetime.timezone.utc).isoformat(),
                },
            }
        )


@routes.put("/{catalog}")
async def handle_catalog_put(request: web.Request) -> web.Response:
    catalog_name = request.match_info["catalog"]
    async with get_db_engine(request).begin() as db:
        await create_catalog(db, catalog_name)
    return web.json_response({"catalog": catalog_name})


@routes.patch("/{catalog}")
async def handle_catalog_patch(request: web.Request) -> web.Response:
    catalog_name = request.match_info["catalog"]
    response = {
        "catalog": catalog_name,
    }
    return web.json_response(response)


@routes.delete("/{catalog}")
async def handle_catalog_delete(request: web.Request) -> web.Response:
    catalog_name = request.match_info["catalog"]
    async with get_db_engine(request).begin() as db:
        await delete_catalog(db, catalog_name)
    return web.json_response({})


@routes.get("/{catalog}/_doc/{id}")
async def get_document(request: web.Request) -> web.Response:
    catalog_name = request.match_info["catalog"]
    doc_id = request.match_info["id"]
    response = {
        "catalog": catalog_name,
        "id": doc_id,
    }
    return web.json_response(response)


@routes.put("/{catalog}/_doc/{id}")
async def create_document(request: web.Request) -> web.Response:
    catalog_name = request.match_info["catalog"]
    doc_id = request.match_info["id"]
    response = {
        "catalog": catalog_name,
        "id": doc_id,
    }
    return web.json_response(response)


@routes.delete("/{catalog}/_doc/{id}")
async def delete_document(request: web.Request) -> web.Response:
    catalog_name = request.match_info["catalog"]
    doc_id = request.match_info["id"]
    response = {
        "catalog": catalog_name,
        "id": doc_id,
    }
    return web.json_response(response)


@routes.get("/{catalog}/_search")
async def search(request: web.Request) -> web.Response:
    catalog_name = request.match_info["catalog"]
    response = {
        "catalog": catalog_name,
    }
    return web.json_response(response)


@routes.get("/{catalog}/_bulk")
async def bulk(request: web.Request) -> web.Response:
    catalog_name = request.match_info["catalog"]
    response = {
        "catalog": catalog_name,
    }
    return web.json_response(response)
