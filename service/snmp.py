from utils.objects import SnmpReply
from pysnmp.hlapi.asyncio import *
from pysnmp.error import PySnmpError


class Snmp:
    def __init__(self):
        pass

    @staticmethod
    async def get_snmp_value(oid: tuple, host_ip='192.168.63.10') -> SnmpReply:
        try:
            error_indication, error_status, error_index, var_binds = \
                await getCmd(SnmpEngine(), CommunityData('public'),
                             UdpTransportTarget((host_ip, 161)),
                             ContextData(),
                             ObjectType(ObjectIdentity(oid))
                             )
            print(error_indication, error_status, error_index, var_binds)
        except PySnmpError:
            return SnmpReply(has_error=True, error="PySnmpError has been raised in get_snmp_value method")

        if error_indication:
            return SnmpReply(has_error=True, error=error_status)

        print(var_binds[0].prettyPrint())

        if "No Such Object currently exists at this OID" in var_binds[0].prettyPrint():
            return SnmpReply(has_error=True, error="No Such Object currently exists at this OID")
        return SnmpReply(has_error=False, error="", value=snmp_value)

    @staticmethod
    async def get_snmp_bulk(oid: tuple,  host_ip='192.168.63.10') -> SnmpReply:
        try:
            error_indication, error_status, error_index, var_binds = \
                await bulkCmd(SnmpEngine(), CommunityData('public'),
                              UdpTransportTarget((host_ip, 161)),
                              ContextData(),
                              0, 25,
                              ObjectType(ObjectIdentity(oid))
                              )
            print(error_indication, error_status, error_index, var_binds)
        except PySnmpError:
            return SnmpReply(has_error=True, error="PySnmpError has been raised in get_snmp_bulk method")

        if error_indication:
            return SnmpReply(has_error=True, error=error_status)

        snmp_value = list()
        for var_bind in var_binds:
            snmp_value.append(var_bind[0].prettyPrint())

        if "No Such Object currently exists at this OID" in (value for value in snmp_value):
            return SnmpReply(has_error=True, error="No Such Object currently exists at this OID")

        return SnmpReply(has_error=False, error="", value=snmp_value)
