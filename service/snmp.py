import asyncio
from pysnmp.hlapi.asyncio import *


async def get_snmp_value(oid: tuple) -> str:
    try:
        error_indication, error_status, error_index, var_binds = \
            await getCmd(SnmpEngine(), CommunityData('public'),
                         UdpTransportTarget(('192.168.63.10', 161)),
                         ContextData(),
                         ObjectType(ObjectIdentity(oid))
                         )
        print(error_indication, error_status, error_index, var_binds)

        if not error_indication:
            snmp_value = ''
            for var_bind in var_binds:
                snmp_value += var_bind.prettyPrint() + '\n'
            if "No Such Object currently exists at this OID" in snmp_value:
                return False
            else:
                return snmp_value
    except:
        return False


# res = asyncio.get_event_loop().run_until_complete(get_snmp_value((1, 3)))
