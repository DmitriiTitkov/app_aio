import aiohttp_jinja2
from aiohttp_session import get_session
from aiohttp import web


@aiohttp_jinja2.template("auth.html")
async def auth_get(request: web.Request):
    db = request.app['database']
    users = await db.users.get_user('test')
    print(request.get("user", None))
    print(request.get("last_vizited", None))
    return {'users': users}


async def auth_post(request: web.Request):
    # TODO Authentification
    authentificated = True

    print("we are here")

    if authentificated:
        session = await get_session(request)
        session['user'] = "test"
    return web.json_response([], status=200)




