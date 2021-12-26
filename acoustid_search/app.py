from aiohttp import web

from acoustid_search.handlers import routes


async def create_app() -> web.Application:
    app = web.Application()
    app.router.add_routes(routes)
    return app


if __name__ == '__main__':
    web.run_app(create_app())
