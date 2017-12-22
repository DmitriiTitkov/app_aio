from aiohttp import web
from service.snmp import get_snmp_value
import re
import aiohttp_jinja2


@aiohttp_jinja2.template('home.html')
async def home(request: web.Request):
    return {'test': ""}


@aiohttp_jinja2.template('home.html')
async def home_post(request: web.Request):

    data = await request.post()
    oid = data.get("snmp_oid")

    # validation
    if not oid:
        return web.HTTPBadRequest(reason="OID is empty")
    valid_oid_symbols = re.compile('\.|\d')

    if not valid_oid_symbols.match(oid):
        return web.HTTPBadRequest(reason="OID is not Valid")

    if len(oid) == 1:
        oid = tuple(oid)
    snmp_result = await get_snmp_value(oid)
    if snmp_result:
        return {'test': snmp_result}
    return {'test': "Nothing was found. Check if the OID correct."}



