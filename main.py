import asyncio
import aiohttp_session
from aiohttp_session import get_session
from aiohttp_session.redis_storage import RedisStorage
from aiohttp import web
from routes import add_routes
from service.snmp import Snmp
import json
import aiohttp_jinja2
import jinja2
import aioredis
from model.database import Database
import datetime


async def get_redis_pool(*args):
    return await aioredis.create_pool('redis://localhost', minsize=5, maxsize=10)


@web.middleware
async def error_middleware(request: web.Request, handler):
    try:
        response: web.Response = await handler(request)
        return response
    except web.HTTPException as ex:
        if ex.status != 404:
            raise
        message = ex.reason
    return web.json_response({'error': message})


@web.middleware
async def user_middleware(request: web.Request, handler):
    session = await get_session(request)
    if not session.empty:
        session['last_vizited'] = datetime.datetime.now().isoformat()
    if session.get('user', None):
        request["user"] = session['user']
        request['last_vizited'] = session['last_vizited']

    return await handler(request)


loop = asyncio.get_event_loop()
redis = loop.run_until_complete(get_redis_pool())
storage = RedisStorage(redis)
session_middleware = aiohttp_session.session_middleware(storage)

app = web.Application(middlewares=[session_middleware, error_middleware, user_middleware])
add_routes(app)
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))
app['database_config'] = json.load(open('config/database.json'))
app['snmp'] = Snmp("192.168.63.10", 161, "public")

app.on_startup.append(Database.create)
app.on_cleanup.append(Database.close)

# web.run_app(app)
web.run_app(app, host='192.168.63.10', port=8080)
