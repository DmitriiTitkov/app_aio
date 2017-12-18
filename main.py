from aiohttp import web
from routes import add_routes
import sysconfig
import routes
import aiohttp_jinja2
import jinja2

print(sysconfig.get_python_version())


app = web.Application()
routes.add_routes(app)
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))

# web.run_app(app)
web.run_app(app, host='192.168.63.10', port=8080)
