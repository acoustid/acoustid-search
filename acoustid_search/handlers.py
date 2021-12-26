import datetime
from typing import Type, Dict, Any

from aiohttp import web
from sqlalchemy.ext.asyncio import AsyncEngine as DatabaseEngine, AsyncConnection as DatabaseConnection

from acoustid_search.db.operations import get_catalog, create_catalog, delete_catalog
from acoustid_search.types import CatalogInfo

routes = web.RouteTableDef()


def json_error(error_cls: Type[web.HTTPException], error_type: str, error_message: str) -> web.HTTPException:
    response = web.json_response(
        {"error": {"type": error_type, "message": error_message}}, status=error_cls.status_code
    )
    return error_cls(headers=response.headers, body=response.body)


def get_db_engine(request: web.Request) -> DatabaseEngine:
    return request.app["db"]


def get_catalog_name(request: web.Request) -> str:
    name = request.match_info["catalog"]
    if name.startswith("_"):
        raise json_error(web.HTTPBadRequest, "invalid_catalog_name", "Catalog name cannot start with '_'")
    if len(name) > 64:
        raise json_error(web.HTTPBadRequest, "invalid_catalog_name", "Catalog name cannot be longer than 64 characters")
    if name != name.lower():
        raise json_error(web.HTTPBadRequest, "invalid_catalog_name", "Catalog name must be lowercase")
    return name


async def get_catalog_or_404(db_conn: DatabaseConnection, catalog_name: str) -> CatalogInfo:
    catalog = await get_catalog(db_conn, catalog_name)
    if catalog is None:
        raise json_error(web.HTTPNotFound, "catalog_not_found", f"Catalog '{catalog_name}' not found")
    return catalog


def serialize_catalog_info(catalog: CatalogInfo) -> Dict[str, Any]:
    return {
        "catalog": catalog.name,
        "status": {
            "created_at": catalog.created_at.astimezone(datetime.timezone.utc).isoformat(),
            "last_modified_at": catalog.last_modified_at.astimezone(datetime.timezone.utc).isoformat(),
        },
    }


@routes.get("/{catalog}")
async def handle_catalog_get(request: web.Request) -> web.Response:
    catalog_name = get_catalog_name(request)
    async with get_db_engine(request).connect() as db_conn:
        catalog = await get_catalog_or_404(db_conn, catalog_name)
        return web.json_response(serialize_catalog_info(catalog))


@routes.put("/{catalog}")
async def handle_catalog_put(request: web.Request) -> web.Response:
    catalog_name = get_catalog_name(request)
    async with get_db_engine(request).begin() as db_conn:
        await create_catalog(db_conn, catalog_name)
        catalog = await get_catalog_or_404(db_conn, catalog_name)
        return web.json_response(serialize_catalog_info(catalog))


@routes.patch("/{catalog}")
async def handle_catalog_patch(request: web.Request) -> web.Response:
    catalog_name = get_catalog_name(request)
    async with get_db_engine(request).begin() as db_conn:
        catalog = await get_catalog_or_404(db_conn, catalog_name)
        return web.json_response(serialize_catalog_info(catalog))


@routes.delete("/{catalog}")
async def handle_catalog_delete(request: web.Request) -> web.Response:
    catalog_name = get_catalog_name(request)
    async with get_db_engine(request).begin() as db:
        await delete_catalog(db, catalog_name)
        return web.json_response({})


@routes.get("/{catalog}/_doc/{id}")
async def get_document(request: web.Request) -> web.Response:
    catalog_name = get_catalog_name(request)
    doc_id = request.match_info["id"]
    async with get_db_engine(request).connect() as db_conn:
        catalog = await get_catalog_or_404(db_conn, catalog_name)
        response = {
            "catalog": catalog.name,
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
