from aiohttp import web
from aiohttp import hdrs
import handlers.html
import handlers.auth


def add_routes(app: web.Application) -> None:

    ar = app.router.add_route
    ar(hdrs.METH_GET, '/', handlers.html.home)
    ar(hdrs.METH_GET, '/auth', handlers.auth.auth_get)
    ar(hdrs.METH_POST, '/auth', handlers.auth.auth_post)
    ar(hdrs.METH_GET, '/auth/logout', handlers.auth.logout)
    ar(hdrs.METH_POST, '/snmp/get_by_oid', handlers.html.get)
    ar(hdrs.METH_POST, '/snmp/getBulk_by_oid', handlers.html.bulk_walk)
