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
        var_binds = [ObjectType(ObjectIdentity(oid))]
        snmp_value = []
        while True:
            try:
                error_indication, error_status, error_index, varBindTable = \
                    await bulkCmd(snmpEngine, CommunityData(self.comunity_string),
                                  UdpTransportTarget((self.ip, self.port)),
                                  ContextData(),
                                  0, 2,
                                  *var_binds
                                  )

                if error_indication:
                    return SnmpReply(has_error=True, error=error_indication)
                if error_status:
                    return SnmpReply(has_error=True, error=error_status)

            except PySnmpError:
                return SnmpReply(has_error=True, error="PySnmpError has been raised in bulk_walk method")

            var_binds = varBindTable[-1]
            if isEndOfMib(var_binds):
                break

            for var_bind_row in varBindTable:
                for var_bind in var_bind_row:
                    snmp_value.append(" = ".join(
                        x.prettyPrint() for x in var_bind)
                    )

        for value in snmp_value:
            if "No Such Object currently exists at this OID" in value:
                return SnmpReply(has_error=True, error="No Such Object currently exists at this OID")

        return SnmpReply(has_error=False, error="", value=snmp_value)

