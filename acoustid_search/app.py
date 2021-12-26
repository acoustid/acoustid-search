from typing import Optional

from aiohttp import web
from sqlalchemy.ext.asyncio import AsyncEngine

from acoustid_search.handlers import routes


def create_app(db_engine: Optional[AsyncEngine] = None) -> web.Application:
    app = web.Application()
    app["db"] = db_engine
    app.router.add_routes(routes)
    return app


if __name__ == "__main__":
    web.run_app(create_app())
