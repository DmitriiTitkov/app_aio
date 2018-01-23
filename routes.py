from aiohttp import web
import handlers.html
import handlers.auth


def add_routes(app: web.Application) -> None:
    ar = app.router.add_get
    ar('/', handlers.html.home)
    ar('/auth', handlers.auth.auth_get)
    app.router.add_post('/snmp/get_by_oid', handlers.html.get_by_oid)
    app.router.add_post('/snmp/getBulk_by_oid', handlers.html.get_by_oid_bulk)
