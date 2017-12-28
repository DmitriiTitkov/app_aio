import aiohttp_jinja2
from aiohttp import web


@aiohttp_jinja2.template("auth.html")
def auth_get(request: web.Request):
    return {}

