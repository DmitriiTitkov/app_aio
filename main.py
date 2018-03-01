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
from model import Database
import datetime
import asyncpg
import os
from typing import Callable
from aiohttp_apiset.middlewares import jsonify
from aiohttp_apiset import SwaggerRouter


async def get_redis_pool() -> aioredis.pool.ConnectionsPool:
    return await aioredis.create_pool('redis://localhost', minsize=5, maxsize=10)


async def create_pool(config: dict =json.load(open('config.json'))) -> asyncpg.pool.Pool:
    return await asyncpg.create_pool(config["databaseconfig"]["dsn"],
                                     min_size=config["databaseconfig"]["minsize"],
                                     timeout=config["databaseconfig"]["timeout"])


@web.middleware
async def error_middleware(request: web.Request, handler: Callable) -> web.Response:
    try:
        response: web.Response = await handler(request)
        return response
    except web.HTTPException as ex:
        if ex.status != 404:
            raise
        message = ex.reason
    return web.json_response({'error': message})


@web.middleware
async def user_middleware(request: web.Request, handler: Callable)-> web.Response:
    session = await get_session(request)
    if not session.empty:
        session['last_visited'] = datetime.datetime.now().isoformat()
    if session.get('user', None):
        request["user"] = session['user']
        request['last_visited'] = session['last_visited']

    return await handler(request)


loop = asyncio.get_event_loop()
pg_pool = loop.run_until_complete(create_pool())
db = Database(pg_pool)
redis = loop.run_until_complete(get_redis_pool())

storage = RedisStorage(redis)
session_middleware = aiohttp_session.session_middleware(storage)

dir_path = os.path.dirname(os.path.realpath(__file__))
router = SwaggerRouter(search_dirs=[dir_path], swagger_ui='/api/', default_validate=True)

app = web.Application(router=router, middlewares=[session_middleware, error_middleware, user_middleware, jsonify])
add_routes(app)
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))

app['database'] = db
app['snmp'] = Snmp("192.168.63.10", 161, "public")
# setup_swagger(app)
app.on_cleanup.append(Database.close)

# web.run_app(app)
web.run_app(app, host='192.168.63.10', port=8080)
