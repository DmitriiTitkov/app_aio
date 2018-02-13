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
    return oid and valid_oid_symbols.match(oid) and len(oid) > 1


async def get(request: web.Request):

    print(await request.text())
    json_data = await request.json()
    oid = json_data.get("snmp_oid", None)

    # validation
    if not await validate_oid(oid):
        return web.HTTPBadRequest(reason="OID is not Valid")

    snmp_result: SnmpReply = await request.app['snmp'].get(oid)

    if snmp_result.has_error:
        return web.HTTPBadRequest(reason="An error occured in snmp request. Check if the OID correct. Error: " + snmp_result.error)
    reply = {'SnmpReply': snmp_result.value}
    return web.json_response(reply, status=200)


async def bulk_walk(request: web.Request):

    print(await request.text())
    json_data = await request.json()
    oid = json_data.get("snmp_oid", None)

    # validation

    if not await validate_oid(oid):
        return web.HTTPBadRequest(reason="OID is not Valid")

    snmp_result: SnmpReply = await request.app['snmp'].bulk_walk(oid)

    if snmp_result.has_error:
        return web.HTTPBadRequest(reason="An error occured in snmp request. Check if the OID correct. Error: " + snmp_result.error)
    reply = {'SnmpReply': snmp_result.value}
    return web.json_response(reply, status=200)
