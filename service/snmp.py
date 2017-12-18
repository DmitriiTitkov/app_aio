import asyncio
from pysnmp.hlapi.asyncio import *


async def get_snmp_value(oid: int) -> str:
    error_indication, error_status, error_index, var_binds = \
        await getCmd(SnmpEngine(), CommunityData('public'),
                     UdpTransportTarget(('192.168.63.10', 161)),
                     ContextData(),
                     ObjectType(ObjectIdentity('SNMPv2-MIB', oid, 0))
                     )
    if not error_indication:
        snmp_value = ''
        for var_bind in var_binds:
            snmp_value += var_bind.prettyPrint() + '\n'

    return snmp_value


# res = asyncio.get_event_loop().run_until_complete(get_snmp_value(1))
