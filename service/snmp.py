from utils.objects import SnmpReply
from pysnmp.hlapi.asyncio import *
from pysnmp.error import PySnmpError


class Snmp:
    def __init__(self, ip: str, port: int, comunity_string):
        self.ip = ip
        self.port = port
        self.comunity_string = comunity_string

    async def get(self, oid: tuple) -> SnmpReply:
        try:
            error_indication, error_status, error_index, var_binds = \
                await getCmd(SnmpEngine(), CommunityData(self.comunity_string),
                             UdpTransportTarget((self.ip, self.port)),
                             ContextData(),
                             ObjectType(ObjectIdentity(oid))
                             )
            print(error_indication, error_status, error_index, var_binds)
        except PySnmpError:
            return SnmpReply(has_error=True, error="PySnmpError has been raised in get_snmp_value method")

        if error_indication:
            return SnmpReply(has_error=True, error=error_status)

        result = var_binds[0].prettyPrint()

        if "No Such Object currently exists at this OID" in result:
            return SnmpReply(has_error=True, error="No Such Object currently exists at this OID")
        return SnmpReply(has_error=False, error="", value=result)

    async def bulk_walk(self, oid: tuple) -> SnmpReply:
        snmpEngine = SnmpEngine()
        var_binds = ObjectType(ObjectIdentity(oid))
        while True:
            try:
                error_indication, error_status, error_index, varBindTable = \
                    await bulkCmd(snmpEngine, CommunityData(self.comunity_string),
                                  UdpTransportTarget((self.ip, self.port)),
                                  ContextData(),
                                  0, 5,
                                  var_binds
                                  )
                # print(error_indication, error_status, error_index, var_binds)
                print(isEndOfMib(varBindTable[-1]))
            except PySnmpError:
                return SnmpReply(has_error=True, error="PySnmpError has been raised in get_snmp_bulk method")

            var_binds = varBindTable[-1]
            if isEndOfMib(var_binds):
                break

        if error_indication:
            return SnmpReply(has_error=True, error=error_status)

        snmp_value = [var_bind[0].prettyPrint() for var_bind in var_binds]
        for value in snmp_value:
            if "No Such Object currently exists at this OID" in value:
                return SnmpReply(has_error=True, error="No Such Object currently exists at this OID")

        return SnmpReply(has_error=False, error="", value=snmp_value)

    async def __bulk_walk(self, oid: tuple) -> SnmpReply:
        try:
            error_indication, error_status, error_index, var_binds = \
                await bulkCmd(SnmpEngine(), CommunityData(self.comunity_string),
                              UdpTransportTarget((self.ip, self.port)),
                              ContextData(),
                              0, 25,
                              ObjectType(ObjectIdentity(oid))
                              )
            print(error_indication, error_status, error_index, var_binds)
        except PySnmpError:
            return SnmpReply(has_error=True, error="PySnmpError has been raised in get_snmp_bulk method")

        if error_indication:
            return SnmpReply(has_error=True, error=error_status)

        snmp_value = [var_bind[0].prettyPrint() for var_bind in var_binds]
        for value in snmp_value:
            if "No Such Object currently exists at this OID" in value:
                return SnmpReply(has_error=True, error="No Such Object currently exists at this OID")

        return SnmpReply(has_error=False, error="", value=snmp_value)
