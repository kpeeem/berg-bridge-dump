# 2016.01.27 00:42:59 MSK
import zcl
import struct
import ezsp

class TunnelingServer:
    _tunnels_inUse = False

    def _tunnelingClusterRequestTunnelCallback(self, protocolId, manufacturerCode, flowControlSupport):
        print 'Rx: Request tunnel 0x%02x 0x%04x 0x%02x' % (protocolId, manufacturerCode, flowControlSupport)
        status = zcl.EMBER_ZCL_TUNNELING_TUNNEL_STATUS_SUCCESS
        tunnelId = 1
        self._tunnels_inUse = True
        (status, self._tunnels_client,) = self.emberLookupEui64ByNodeId(self._currentCommand.source)
        self._tunnels_clientEndpoint = self._currentCommand.apsFrame.sourceEndpoint
        self._tunnels_serverEndpoint = self._currentCommand.apsFrame.destinationEndpoint
        if status == zcl.EMBER_ZCL_TUNNELING_TUNNEL_STATUS_SUCCESS:
            self.callback_afTunnelingServerTunnelOpened(tunnelId, protocolId, manufacturerCode)
        self._fillCommandTunnelingClusterRequestTunnelResponse(tunnelId, status)
        self._responseApsFrame.options |= ezsp.EMBER_APS_OPTION_SOURCE_EUI64
        self._sendResponse()
        return True



    def _fillCommandTunnelingClusterRequestTunnelResponse(self, tunnelId, status):
        frameControl = zcl.ZCL_CLUSTER_SPECIFIC_COMMAND | zcl.ZCL_FRAME_CONTROL_SERVER_TO_CLIENT
        sequence = self._incomingZclSequenceNumber
        commandId = zcl.ZCL_REQUEST_TUNNEL_RESPONSE_COMMAND_ID
        self._responseData = struct.pack('<BBBHB', frameControl, sequence, commandId, tunnelId, status)
        self._responseApsFrame.clusterId = zcl.ZCL_TUNNELING_CLUSTER_ID



    def _fillCommandTunnelingClusterTransferDataErrorServerToClient(self, tunnelId, status):
        frameControl = zcl.ZCL_CLUSTER_SPECIFIC_COMMAND | zcl.ZCL_FRAME_CONTROL_SERVER_TO_CLIENT
        sequence = self._incomingZclSequenceNumber
        commandId = zcl.ZCL_TRANSFER_DATA_ERROR_SERVER_TO_CLIENT_COMMAND_ID
        self._responseData = struct.pack('<BBBHB', frameControl, sequence, commandId, tunnelId, status)
        self._responseApsFrame.clusterId = zcl.ZCL_TUNNELING_CLUSTER_ID



    def _fillCommandTunnelingClusterTransferDataServerToClient(self, tunnelId, data):
        frameControl = zcl.ZCL_CLUSTER_SPECIFIC_COMMAND | zcl.ZCL_FRAME_CONTROL_SERVER_TO_CLIENT
        sequence = self._incomingZclSequenceNumber
        commandId = zcl.ZCL_TRANSFER_DATA_SERVER_TO_CLIENT_COMMAND_ID
        self._tunnelData = struct.pack('<BBBH', frameControl, sequence, commandId, tunnelId) + data



    def _tunnelingServerTransferData(self, tunnelId, data):
        if self._tunnels_inUse == True:
            nodeId = self.emberLookupNodeIdByEui64(self._tunnels_client)
            self._fillCommandTunnelingClusterTransferDataServerToClient(tunnelId, data)
            apsFrame = ezsp.EmberApsFrame()
            apsFrame.profileId = 49152
            apsFrame.clusterId = zcl.ZCL_TUNNELING_CLUSTER_ID
            apsFrame.sourceEndpoint = self._tunnels_serverEndpoint
            apsFrame.destinationEndpoint = self._tunnels_clientEndpoint
            apsFrame.options = self.EMBER_AF_DEFAULT_APS_OPTIONS | ezsp.EMBER_APS_OPTION_SOURCE_EUI64
            status = self.sendUnicast(ezsp.EMBER_OUTGOING_DIRECT, nodeId, apsFrame, self._tunnelData)
            if status == ezsp.EMBER_SUCCESS:
                return zcl.EMBER_ZCL_STATUS_SUCCESS
            else:
                return zcl.EMBER_ZCL_STATUS_FAILURE
        return zcl.EMBER_ZCL_STATUS_NOT_FOUND



    def _tunnelingClusterTransferDataClientToServerCallback(self, tunnelId, data):
        if tunnelId == 1 and self._tunnels_inUse == True:
            self.callback_afTunnelingServerDataReceived(tunnelId, data)
            self.sendDefaultResponse(self._currentCommand, zcl.EMBER_ZCL_STATUS_SUCCESS)
        else:
            self._fillCommandTunnelingClusterTransferDataErrorServerToClient(tunnelId, zcl.EMBER_ZCL_TUNNELING_TRANSFER_DATA_STATUS_NO_SUCH_TUNNEL)
            self._responseApsFrame.options |= ezsp.EMBER_APS_OPTION_SOURCE_EUI64
            self._sendResponse()
        return True




+++ okay decompyling ./tunneling_server.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2016.01.27 00:42:59 MSK
