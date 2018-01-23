import aiohttp_jinja2
from aiohttp import web


@aiohttp_jinja2.template("auth.html")
async def auth_get(request: web.Request):
    db = request.app['database']
    users = await db.users.get_user('test')
    print(users)
    return {'users': users}

