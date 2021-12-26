from aiohttp import web

routes = web.RouteTableDef()


@routes.get('/')
async def index(request: web.Request) -> web.Response:
    return web.Response(text='Hello, world!2')
