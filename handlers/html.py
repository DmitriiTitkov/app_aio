from aiohttp import web
from service.snmp import get_snmp_value
import templates
import aiohttp_jinja2



def template(*args):
    def wrapper():
        return web.web_fileresponse(templates.html)

    return wrapper


@aiohttp_jinja2.template('home.html')
async def home(request: web.Request):
    return {'test': ""}

@aiohttp_jinja2.template('home.html')
async def home_post(request: web.Request):
    # Some Validation here
    data = await request.post()
    print(data)
    testget = await get_snmp_value("sysDescr")
    return {'test': testget}
