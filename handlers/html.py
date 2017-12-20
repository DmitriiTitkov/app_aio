from aiohttp import web
from service.snmp import get_snmp_value
import templates
import aiohttp_jinja2
import string


def template(*args):
    def wrapper():
        return web.web_fileresponse(templates.html)

    return wrapper


@aiohttp_jinja2.template('home.html')
async def home(request: web.Request):
    return {'test': ""}


@aiohttp_jinja2.template('home.html')
async def home_post(request: web.Request):

    data = request.post()
    oid = data.get("snmp_oid")

    # validation
    valid_oid_symbols = set(string.digits + ".")
    if set(oid) <= valid_oid_symbols and oid:
        if len(oid) == 1:
            oid = tuple(oid)

        snmp_result = await get_snmp_value(oid)
        if snmp_result:
            return {'test': snmp_result}
        else:
            return {'test': "Nothing was found. Check if the OID correct."}
    else:
        return {'test': "OID is not valid. OID should contain only digits and '.'."}

