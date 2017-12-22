from utils.objects import SnmpReply
from pysnmp.hlapi.asyncio import *


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
        except:
            return SnmpReply(has_error=True, error="")

        if error_indication:
            return SnmpReply(has_error=True, error="")

        snmp_value = var_binds[0].prettyPrint()
        if "No Such Object currently exists at this OID" in snmp_value:
            return False
        return snmp_value


# TODO get snmp subtree
# res = asyncio.get_event_loop().run_until_complete(get_snmp_value((1, 3)))
