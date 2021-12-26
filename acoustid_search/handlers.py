from typing import Dict, Any

from aiohttp import web

routes = web.RouteTableDef()


@routes.get("/{index}")
async def get_index(request: web.Request) -> web.Response:
    index_name = request.match_info["index"]
    response = {
        "index": index_name,
    }
    return web.json_response(response)


@routes.put("/{index}")
async def create_index(request: web.Request) -> web.Response:
    index_name = request.match_info["index"]
    response = {
        "index": index_name,
    }
    return web.json_response(response)


@routes.patch("/{index}")
async def update_index(request: web.Request) -> web.Response:
    index_name = request.match_info["index"]
    response = {
        "index": index_name,
    }
    return web.json_response(response)


@routes.delete("/{index}")
async def delete_index(request: web.Request) -> web.Response:
    response: Dict[str, Any] = {}
    return web.json_response(response)


@routes.get("/{index}/_doc/{id}")
async def get_document(request: web.Request) -> web.Response:
    index_name = request.match_info["index"]
    doc_id = request.match_info["id"]
    response = {
        "index": index_name,
        "id": doc_id,
    }
    return web.json_response(response)


@routes.put("/{index}/_doc/{id}")
async def create_document(request: web.Request) -> web.Response:
    index_name = request.match_info["index"]
    doc_id = request.match_info["id"]
    response = {
        "index": index_name,
        "id": doc_id,
    }
    return web.json_response(response)


@routes.delete("/{index}/_doc/{id}")
async def delete_document(request: web.Request) -> web.Response:
    index_name = request.match_info["index"]
    doc_id = request.match_info["id"]
    response = {
        "index": index_name,
        "id": doc_id,
    }
    return web.json_response(response)


@routes.get("/{index}/_search")
async def search(request: web.Request) -> web.Response:
    index_name = request.match_info["index"]
    response = {
        "index": index_name,
    }
    return web.json_response(response)


@routes.get("/{index}/_bulk")
async def bulk(request: web.Request) -> web.Response:
    index_name = request.match_info["index"]
    response = {
        "index": index_name,
    }
    return web.json_response(response)
