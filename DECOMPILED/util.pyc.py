# 2016.01.27 00:43:01 MSK
import ezsp
import config

class Util:

    def maximumApsPayloadLength(self, type, indexOrDestination, apsFrame):
        destination = ezsp.EMBER_UNKNOWN_NODE_ID
        max = self.EMBER_AF_MAXIMUM_APS_PAYLOAD_LENGTH
        if apsFrame.options & ezsp.EMBER_APS_OPTION_ENCRYPTION:
            max -= config.EMBER_AF_APS_ENCRYPTION_OVERHEAD
        if apsFrame.options & ezsp.EMBER_APS_OPTION_SOURCE_EUI64:
            max -= ezsp.EUI64_SIZE
        if apsFrame.options & ezsp.EMBER_APS_OPTION_DESTINATION_EUI64:
            max -= ezsp.EUI64_SIZE
        if apsFrame.options & ezsp.EMBER_APS_OPTION_FRAGMENT:
            max -= config.EMBER_AF_APS_FRAGMENTATION_OVERHEAD
        if type == ezsp.EMBER_OUTGOING_DIRECT:
            destination = indexOrDestination
        elif type == ezsp.EMBER_OUTGOING_VIA_ADDRESS_TABLE:
            destination = emberGetAddressTableRemoteNodeId(indexOrDestination)
        elif type == ezsp.EMBER_OUTGOING_VIA_BINDING:
            destination = emberGetBindingRemoteNodeId(indexOrDestination)
        elif type == ezsp.EMBER_OUTGOING_MULTICAST:
            max -= 1
        elif type == ezsp.EMBER_OUTGOING_BROADCAST:
            pass
        return max




+++ okay decompyling ./util.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2016.01.27 00:43:01 MSK
