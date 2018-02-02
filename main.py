from aiohttp import web
from routes import add_routes
from service.snmp import Snmp
import json
import aiohttp_jinja2
import jinja2
from model.database import Database

app = web.Application()
add_routes(app)
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))
app['database_config'] = json.load(open('config/database.json'))
app['snmp'] = Snmp("192.168.63.10", 161, "public")

app.on_startup.append(Database.create)
app.on_cleanup.append(Database.close)

# web.run_app(app)
web.run_app(app, host='192.168.63.10', port=8080)
