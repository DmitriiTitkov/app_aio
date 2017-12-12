from aiohttp import web
import handlers.html


def add_routes(app: web.Application) -> None:
    ar = app.router.add_get
    ar('/', handlers.html.home)
    app.router.add_post('/', handlers.html.home_post)
    # ar('/test', test)
