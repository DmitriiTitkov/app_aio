from aiohttp import web
from service.snmp import Snmp
from utils.objects import SnmpReply
import re
import aiohttp_jinja2


@aiohttp_jinja2.template('home.html')
async def home(request: web.Request):
    pass


# @aiohttp_jinja2.template('home.html')
async def home_post(request: web.Request):

    data = await request.post()
    oid = data.get("snmp_oid")
    is_bulk = data.get("GetSubtree")
    print(is_bulk)

    # validation
    if not oid:
        return web.HTTPBadRequest(reason="OID is empty")
    valid_oid_symbols = re.compile('^(\.|\d)+$')

    if not valid_oid_symbols.match(oid):
        return web.HTTPBadRequest(reason="OID is not Valid")

    if len(oid) == 1:
        oid = tuple(oid)

    if is_bulk:
        snmp_result: SnmpReply = await Snmp.get_snmp_bulk(oid)
    else:
        snmp_result: SnmpReply = await Snmp.get_snmp_value(oid)

    if snmp_result.has_error:
        return web.HTTPBadRequest(reason="Nothing was found. Check if the OID correct.")
    reply = {'SnmpReply': snmp_result.value}
    return web.json_response(reply, status=200)




