from aiohttp import web
from service.snmp import SnmpReply
import re
import aiohttp_jinja2

valid_oid_symbols = re.compile('^(\.|\d)+$')


async def home(request: web.Request):
    """ Returns default home page
       ---
      tags:
      - Home
      description: Returns home page

      responses:
        '200':
          description: OK
    """
    return aiohttp_jinja2.render_template('home.html', request, {}, app_key=aiohttp_jinja2.APP_KEY, encoding='utf-8')


def validate_oid(oid):
    return oid and valid_oid_symbols.match(oid) and len(oid) > 1


async def get(request: web.Request):
    """ get value by oid from MIB
       ---
      tags:
      - Snmp
      description: get value by oid from MIB
      parameters:
      - name: body
        in: body
        schema:
          type: object
          properties:
            snmp_oid:
              type: string
          required:
            - snmp_oid
      responses:
        '200':
          description: OK
          schema:
            type: object
            properties:
              SnmpReply: string
        '400':
          description: Validation error
    """

    print(await request.text())
    json_data = await request.json()
    oid = json_data.get("snmp_oid", None)

    # validation
    if not validate_oid(oid):
        return web.HTTPBadRequest(reason="OID is not Valid")

    snmp_result: SnmpReply = await request.app['snmp'].get(oid)

    if snmp_result.has_error:
        return web.HTTPBadRequest(
            reason="An error occured in snmp request. Check if the OID correct. Error: " + snmp_result.error)
    reply = {'SnmpReply': snmp_result.value}
    return web.json_response(reply, status=200)


async def bulk_walk(request: web.Request):
    """ Perform bulk walk operation against MIB
       ---
      tags:
      - Snmp
      description: Perform bulk walk operation against MIB
      parameters:
      - name: body
        in: body
        schema:
          type: object
          properties:
            snmp_oid:
              type: string
          required:
            - snmp_oid
      responses:
        '200':
          description: OK
          schema:
            type: object
            properties:
              SnmpReply:
                type: array
        '400':
          description: Validation error
    """
    print(await request.text())
    json_data = await request.json()
    oid = json_data.get("snmp_oid", None)

    # validation

    if not validate_oid(oid):
        return web.HTTPBadRequest(reason="OID is not Valid")

    snmp_result: SnmpReply = await request.app['snmp'].bulk_walk(oid)

    if snmp_result.has_error:
        return web.HTTPBadRequest(
            reason="An error occurred in snmp request. Check if the OID correct. Error: " + snmp_result.error)
    reply = {'SnmpReply': snmp_result.value}
    return web.json_response(reply, status=200)
