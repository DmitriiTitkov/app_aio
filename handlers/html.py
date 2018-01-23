from aiohttp import web
from service.snmp import Snmp
from utils.objects import SnmpReply
import re
import aiohttp_jinja2

valid_oid_symbols = re.compile('^(\.|\d)+$')

@aiohttp_jinja2.template('home.html')
async def home(request: web.Request):
    pass


async def validate_oid(oid):
    if oid and valid_oid_symbols.match(oid) and len(oid) > 1:
        return True
    return False


async def get_by_oid(request: web.Request):
    data = await request.post()
    oid = data.get("snmp_oid")

    # validation
    if not await validate_oid(oid):
        return web.HTTPBadRequest(reason="OID is not Valid")

    snmp_result: SnmpReply = await Snmp.get_snmp_value(oid)

    if snmp_result.has_error:
        return web.HTTPBadRequest(reason="An error occured in snmp request. Check if the OID correct. Error: " + snmp_result.error)
    reply = {'SnmpReply': snmp_result.value}
    return web.json_response(reply, status=200)


async def get_by_oid_bulk(request: web.Request):
    data = await request.post()
    oid = data.get("snmp_oid")
    # validation
    if not await validate_oid(oid):
        return web.HTTPBadRequest(reason="OID is not Valid")

    snmp_result: SnmpReply = await Snmp.get_snmp_bulk(oid)

    if snmp_result.has_error:
        return web.HTTPBadRequest(reason="An error occured in snmp request. Check if the OID correct. Error: " + snmp_result.error)
    reply = {'SnmpReply': snmp_result.value}
    return web.json_response(reply, status=200)
