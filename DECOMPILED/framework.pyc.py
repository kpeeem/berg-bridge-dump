# 2016.01.27 00:42:46 MSK
import ezsp
import ezsp_protocol
import util
import fragmentation
import form_and_join
import security_config
import service_discovery
import zcl
import tunneling_server
import struct
import packet_statistics
import config
import trust_center
import byte_tuple
import network_manager

class EmberAfClusterCommand:
    ZCL_DIRECTION_CLIENT_TO_SERVER = 0
    ZCL_DIRECTION_SERVER_TO_CLIENT = 1
    ZCL_UTIL_RESP_NORMAL = 0
    ZCL_UTIL_RESP_NONE = 1
    ZCL_UTIL_RESP_INTERPAN = 2

    def __init__(self):
        self.apsFrame = ezsp.EmberApsFrame()
        self.type = None
        self.source = None
        self.buffer = None
        self.clusterSpecific = False
        self.mfgSpecific = False
        self.mfgCode = None
        self.seqNum = None
        self.commandId = None
        self.payloadStartIndex = None
        self.direction = None
        self.interPanHeader = None




class ApplicationFramework(fragmentation.Fragmentation, form_and_join.FormAndJoin, service_discovery.ServiceDiscovery, util.Util, tunneling_server.TunnelingServer, trust_center.TrustCenter, network_manager.NetworkManager, ezsp.EZSPInterface):
    _incomingZclSequenceNumber = 0
    _ZDOSequence = 0

    def refreshNodeId(self):
        self._nodeId = self.emberGetNodeId()
        return self._nodeId



    def _getStackProfile(self):
        return self.ezspGetConfigurationValue(ezsp.EZSP_CONFIG_STACK_PROFILE)



    def _setPacketBufferCount(self):
        packetBufferCount = self.ezspGetConfigurationValue(ezsp.EZSP_CONFIG_PACKET_BUFFER_COUNT)
        while True:
            try:
                self.ezspSetConfigurationValue(ezsp.EZSP_CONFIG_PACKET_BUFFER_COUNT, packetBufferCount)
            except ezsp.EzspStatus as e:
                if e.value != ezsp.EZSP_ERROR_OUT_OF_MEMORY:
                    raise 
                self.logger.debug('Config: Set packet buffers to %d' % (packetBufferCount - 1))
                return 
            packetBufferCount += 1




    def _getVersion(self):
        (ncpEzspProtocolVersion, ncpStackType, ncpStackVersion,) = self.ezspVersion(ezsp_protocol.EZSP_PROTOCOL_VERSION)
        self.logger.debug('ezsp ver 0x%02x stack type 0x%02x stack ver 0x%04x' % (ncpEzspProtocolVersion, ncpStackType, ncpStackVersion))
        if ncpStackType != ezsp_protocol.EZSP_STACK_TYPE_MESH:
            self.logger.error('Error: Unexpected stack type')
            return False
        if ncpEzspProtocolVersion != ezsp_protocol.EZSP_PROTOCOL_VERSION:
            self.logger.error('Error: NCP EZSP protocol version does not match Host version')
            return False
        return True



    def _setEzspConfigValue(self, configId, value, configName):
        self.ezspSetConfigurationValue(configId, value)
        self.logger.debug("Config: Set '%s' to 0x%02x" % (configName, value))



    def _setEzspPolicy(self, policyId, decisionId, policyName, decisionName):
        self.ezspSetPolicy(policyId, decisionId)
        self.logger.debug("Policy: Set '%s' to '%s' (0x%02x)" % (policyName, decisionName, decisionId))



    def _setEzspValue(self, valueId, value, valueName):
        self.ezspSetValue(valueId, value)
        self.logger.debug("Value: Set '%s' to %s" % (valueName, str(value)))



    def _createEndpoint(self, ep):
        self.ezspAddEndpoint(ep['endpoint_number'], ep['profile_id'], ep['device_id'], ep['device_version'], ep['in_clusters'], ep['out_clusters'])
        self.logger.debug('Added endpoint %i:' % ep['endpoint_number'])
        self.logger.debug('    Profile ID: 0x%04x' % ep['profile_id'])
        self.logger.debug('    Device ID:  0x%04x' % ep['device_id'])
        self.logger.debug('    Version:    0x%02x' % ep['device_version'])
        self.logger.debug('    In Clustr:  %s' % str(ep['in_clusters']))
        self.logger.debug('    Out Clustr: %s' % str(ep['out_clusters']))



    def _networkInit(self):
        self.emberNetworkInit()



    def _resetAndInitNCP(self):
        self.ezspInit()
        if not self._getVersion():
            return False
        _applicationZdoFlags = 0
        if self.EMBER_APPLICATION_RECEIVES_SUPPORTED_ZDO_REQUESTS:
            _applicationZdoFlags |= ezsp.EMBER_APP_RECEIVES_SUPPORTED_ZDO_REQUESTS
        if self.EMBER_APPLICATION_HANDLES_UNSUPPORTED_ZDO_REQUESTS:
            _applicationZdoFlags |= ezsp.EMBER_APP_HANDLES_UNSUPPORTED_ZDO_REQUESTS
        if self.EMBER_APPLICATION_HANDLES_ENDPOINT_ZDO_REQUESTS:
            _applicationZdoFlags |= ezsp.EMBER_APP_HANDLES_ZDO_ENDPOINT_REQUESTS
        if self.EMBER_APPLICATION_HANDLES_BINDING_ZDO_REQUESTS:
            _applicationZdoFlags |= ezsp.EMBER_APP_HANDLES_ZDO_BINDING_REQUESTS
        self._setEzspConfigValue(ezsp.EZSP_CONFIG_APPLICATION_ZDO_FLAGS, _applicationZdoFlags, 'application zdo flags')
        self._setEzspConfigValue(ezsp.EZSP_CONFIG_SOURCE_ROUTE_TABLE_SIZE, self.EMBER_SOURCE_ROUTE_TABLE_SIZE, 'source route table size')
        self._setEzspConfigValue(ezsp.EZSP_CONFIG_SECURITY_LEVEL, self.SECURITY_LEVEL, 'security level')
        self._setEzspConfigValue(ezsp.EZSP_CONFIG_ADDRESS_TABLE_SIZE, self.EMBER_AF_ADDRESS_TABLE_SIZE, 'address table size')
        self._setEzspConfigValue(ezsp.EZSP_CONFIG_TRUST_CENTER_ADDRESS_CACHE_SIZE, self.EMBER_AF_TRUST_CENTER_ADDRESS_CACHE_SIZE, 'TC addr cache')
        self._setEzspConfigValue(ezsp.EZSP_CONFIG_STACK_PROFILE, self.EMBER_STACK_PROFILE, 'stack profile')
        self._setEzspConfigValue(ezsp.EZSP_CONFIG_KEY_TABLE_SIZE, self.EMBER_KEY_TABLE_SIZE, 'key table size')
        self._setEzspPolicy(ezsp.EZSP_BINDING_MODIFICATION_POLICY, ezsp.EZSP_DISALLOW_BINDING_MODIFICATION, 'binding modify', 'disallow')
        self._setEzspPolicy(ezsp.EZSP_MESSAGE_CONTENTS_IN_CALLBACK_POLICY, ezsp.EZSP_MESSAGE_TAG_ONLY_IN_CALLBACK, 'message content in msgSent', 'Tag only')
        self._setEzspValue(ezsp.EZSP_VALUE_MAXIMUM_INCOMING_TRANSFER_SIZE, (self.EMBER_AF_INCOMING_BUFFER_LENGTH & 255, self.EMBER_AF_INCOMING_BUFFER_LENGTH >> 8), 'maximum incoming transfer size')
        self._setEzspValue(ezsp.EZSP_VALUE_MAXIMUM_OUTGOING_TRANSFER_SIZE, (self.EMBER_AF_MAXIMUM_SEND_PAYLOAD_LENGTH & 255, self.EMBER_AF_MAXIMUM_SEND_PAYLOAD_LENGTH >> 8), 'maximum outgoing transfer size')
        self._setEzspConfigValue(ezsp.EZSP_CONFIG_FRAGMENT_WINDOW_SIZE, 8, 'Fragment window size')
        self._setEzspConfigValue(ezsp.EZSP_CONFIG_FRAGMENT_DELAY_MS, 0, 'Fragment delay')
        self._setEzspConfigValue(ezsp.EZSP_CONFIG_END_DEVICE_POLL_TIMEOUT, self.EMBER_END_DEVICE_POLL_TIMEOUT, 'End device poll timeout')
        self._setEzspConfigValue(ezsp.EZSP_CONFIG_END_DEVICE_POLL_TIMEOUT_SHIFT, self.EMBER_END_DEVICE_POLL_TIMEOUT_SHIFT, 'End device poll timeout shift')
        self._setEzspConfigValue(ezsp.EZSP_CONFIG_TX_POWER_MODE, self.bridge_configuration['tx_power_mode'], 'TX power mode')
        self._setEzspConfigValue(ezsp.EZSP_CONFIG_DISABLE_RELAY, self.bridge_configuration['disable_relay'], 'Disable relay')
        self.logger.info('End device timeout is %i seconds.' % (self.EMBER_END_DEVICE_POLL_TIMEOUT << self.EMBER_END_DEVICE_POLL_TIMEOUT_SHIFT))
        self.emberSetManufacturerCode(self.EMBER_AF_MANUFACTURER_CODE)
        self._setPacketBufferCount()
        if self.EMBER_AF_ENABLE_FRAGMENTATION:
            self.fragmentationInit()
        for ep in self.ENDPOINTS:
            self._createEndpoint(ep)

        self.TCSecurityPolicyInit()
        self._joinedNetwork = False
        parameters = ezsp.EmberNetworkParameters()
        try:
            nodeType = self.ezspGetNetworkParameters(parameters)
            self._joinedNetwork = True
        except ezsp.EmberStatus as e:
            if e.value != ezsp.EMBER_NOT_JOINED:
                raise 
        if self._joinedNetwork:
            if nodeType == self.ZA_DEVICE_TYPE:
                self._networkInit()
            elif nodetype == ezsp.EMBER_ROUTER:
                if self.ZA_DEVICE_TYPE == config.ZA_COORDINATOR:
                    self._networkInit()
        self._eui64 = self.ezspGetEui64()
        return True



    def init(self):
        if self.EMBER_AF_SECURITY_PROFILE == security_config.NONE_SECURITY_PROFILE:
            self.SECURITY_LEVEL = 0
        else:
            self.SECURITY_LEVEL = 5
        if self.EMBER_AF_SECURITY_PROFILE == security_config.NONE_SECURITY_PROFILE:
            self.EMBER_AF_MAXIMUM_APS_PAYLOAD_LENGTH = 100
        else:
            self.EMBER_AF_MAXIMUM_APS_PAYLOAD_LENGTH = 82
        if self.EMBER_AF_ENABLE_FRAGMENTATION == True:
            if self.EMBER_AF_FRAGMENT_BUFFER_SIZE > self.EMBER_AF_MAXIMUM_APS_PAYLOAD_LENGTH:
                self.EMBER_AF_MAXIMUM_SEND_PAYLOAD_LENGTH = self.EMBER_AF_FRAGMENT_BUFFER_SIZE
                self.EMBER_AF_INCOMING_BUFFER_LENGTH = self.EMBER_AF_FRAGMENT_BUFFER_SIZE
            else:
                self.EMBER_AF_MAXIMUM_SEND_PAYLOAD_LENGTH = self.EMBER_AF_MAXIMUM_APS_PAYLOAD_LENGTH
                self.EMBER_AF_INCOMING_BUFFER_LENGTH = self.EMBER_AF_MAXIMUM_APS_PAYLOAD_LENGTH
        if self.EMBER_AF_CONCENTRATOR:
            self.EMBER_AF_DEFAULT_APS_OPTIONS = ezsp.EMBER_APS_OPTION_RETRY | ezsp.EMBER_APS_OPTION_ENABLE_ADDRESS_DISCOVERY
        else:
            self.EMBER_AF_DEFAULT_APS_OPTIONS = ezsp.EMBER_APS_OPTION_RETRY | ezsp.EMBER_APS_OPTION_ENABLE_ROUTE_DISCOVERY | ezsp.EMBER_APS_OPTION_ENABLE_ADDRESS_DISCOVERY
        self._responseData = ''
        self._responseApsFrame = ezsp.EmberApsFrame()
        self._responseDestination = None
        self._responseType = EmberAfClusterCommand.ZCL_UTIL_RESP_INTERPAN
        self._incomingMessagePacketStatsList = []
        if self._resetAndInitNCP() == False:
            return False



    def restartNCP():
        return self._resetAndInitNCP()



    def sendMulticast(self, multicastId, apsFrame, message):
        max = self.maximumApsPayloadLength(ezsp.EMBER_OUTGOING_MULTICAST, multicastId, apsFrame)
        if len(message) > max:
            return ezsp.EMBER_MESSAGE_TOO_LONG
        apsFrame.groupId = multicastId
        apsFrame.sequence = self.ezspSendMulticast(apsFrame, ZA_MAX_HOPS, ZA_MAX_HOPS, 0, message)



    def sendBroadcast(self, destination, apsFrame, message):
        max = self.maximumApsPayloadLength(ezsp.EMBER_OUTGOING_BROADCAST, destination, apsFrame)
        if len(message) > max:
            return ezsp.EMBER_MESSAGE_TOO_LONG
        apsFrame.sequence = self.ezspSendBroadcast(apsFrame, ZA_MAX_HOPS, 0, message)



    def sendUnicast(self, type, indexOrDestination, apsFrame, message):
        max = self.maximumApsPayloadLength(type, indexOrDestination, apsFrame)
        if len(message) > max:
            if self.EMBER_AF_ENABLE_FRAGMENTATION:
                self.fragmentationSendUnicast(type, indexOrDestination, apsFrame, message)
            else:
                raise ezsp.EmberStatus(ezsp.EMBER_MESSAGE_TOO_LONG)
        else:
            apsFrame.sequence = self.ezspSendUnicast(type, indexOrDestination, apsFrame, 0, message)



    def _getNextZDORequestSequence(self):
        APPLICATION_ZDO_SEQUENCE_MASK = 127
        self._ZDOSequence += 1
        return self._ZDOSequence & APPLICATION_ZDO_SEQUENCE_MASK



    def _sendZDORequestBuffer(self, destination, clusterId, options, request):
        apsFrame = ezsp.EmberApsFrame()
        apsFrame.sourceEndpoint = ezsp.EMBER_ZDO_ENDPOINT
        apsFrame.destinationEndpoint = ezsp.EMBER_ZDO_ENDPOINT
        apsFrame.clusterId = clusterId
        apsFrame.profileId = ezsp.EMBER_ZDO_PROFILE_ID
        apsFrame.options = options
        if destination == ezsp.EMBER_BROADCAST_ADDRESS or destination == ezsp.EMBER_RX_ON_WHEN_IDLE_BROADCAST_ADDRESS or destination == ezsp.EMBER_SLEEPY_BROADCAST_ADDRESS:
            return self.sendBroadcast(destination, apsFrame, reequest)
        else:
            return self.sendUnicast(ezsp.EMBER_OUTGOING_DIRECT, destination, apsFrame, request)



    def afRemoveDevice(self, nodeId, rejoin = False, removeChildren = False):
        options = 0
        if rejoin:
            options |= 128
        if removeChildren:
            options |= 64
        request = struct.pack('<BQB', self._getNextZDORequestSequence(), 0, options)
        return self._sendZDORequestBuffer(nodeId, ezsp.LEAVE_REQUEST, self.EMBER_AF_DEFAULT_APS_OPTIONS, request)



    def _tunnelingClusterServerCommandParse(self, cmd):
        wasHandled = False
        if cmd.commandId == zcl.ZCL_REQUEST_TUNNEL_COMMAND_ID:
            payloadOffset = cmd.payloadStartIndex
            if len(cmd.buffer) < 7:
                return zcl.EMBER_ZCL_STATUS_MALFORMED_COMMAND
            (protocolId, manufacturerCode, flowControlSupport,) = struct.unpack_from('<BHB', cmd.buffer, payloadOffset)
            wasHandled = self._tunnelingClusterRequestTunnelCallback(protocolId, manufacturerCode, flowControlSupport)
        elif cmd.commandId == zcl.ZCL_TRANSFER_DATA_CLIENT_TO_SERVER_COMMAND_ID:
            payloadOffset = cmd.payloadStartIndex
            if len(cmd.buffer) < 5:
                return zcl.EMBER_ZCL_STATUS_MALFORMED_COMMAND
            (tunnelId,) = struct.unpack_from('<H', cmd.buffer, payloadOffset)
            payloadOffset += 2
            data = cmd.buffer[payloadOffset:]
            wasHandled = self._tunnelingClusterTransferDataClientToServerCallback(tunnelId, data)
        if wasHandled:
            return zcl.EMBER_ZCL_STATUS_SUCCESS
        return zcl.EMBER_ZCL_STATUS_UNSUP_CLUSTER_COMMAND



    def _weminuchCommandParse(self, cmd):
        wasHandled = False
        if cmd.commandId == 1:
            payloadOffset = cmd.payloadStartIndex
            if len(cmd.buffer) < 5:
                return zcl.EMBER_ZCL_STATUS_MALFORMED_COMMAND
            data = cmd.buffer[payloadOffset:]
            (eventCode,) = struct.unpack_from('<H', data, 0)
            if eventCode == 128:
                wasHandled = self._weminucheCommandResponseCallback(self._currentSenderEui64, data, self.currentMessagePacketStatsList)
            else:
                wasHandled = self._weminucheEventCallback(self._currentSenderEui64, data, self.currentMessagePacketStatsList)
        if wasHandled:
            return zcl.EMBER_ZCL_STATUS_SUCCESS
        return zcl.EMBER_ZCL_STATUS_UNSUP_CLUSTER_COMMAND



    def _clusterSpecificCommandParse(self, cmd):
        if cmd.direction == EmberAfClusterCommand.ZCL_DIRECTION_SERVER_TO_CLIENT:
            if cmd.apsFrame.clusterId == 65280:
                return self._weminuchCommandParse(cmd)
        return zcl.EMBER_ZCL_STATUS_UNSUP_CLUSTER_COMMAND



    def _sendZclMessage(self, request):
        if request:
            sequenceNumber = self._nextSequence()
        else:
            sequenceNumber = self._incomingZclSequenceNumber
        if self._responseType & EmberAfClusterCommand.ZCL_UTIL_RESP_INTERPAN:
            type = 'InterPAN'
        elif self._responseDestination < ezsp.EMBER_BROADCAST_ADDRESS:
            label = 'Unicast'
            self.sendUnicast(ezsp.EMBER_OUTGOING_DIRECT, self._responseDestination, self._responseApsFrame, self._responseData)
        else:
            label = 'Broadcast'
            self.sendBroadcast(self._responseDestination, self._responseApsFrame, self._responseData)
        self._responseWaitingFlag = False



    def _sendResponse(self):
        if self._responseType & EmberAfClusterCommand.ZCL_UTIL_RESP_NONE:
            self._responseWaitingFlag = False
        else:
            self._sendZclMessage(False)



    def _prepareForResponse(self, cmd):
        self._responseApsFrame.profileId = cmd.apsFrame.profileId
        self._responseApsFrame.clusterId = cmd.apsFrame.clusterId
        self._responseApsFrame.sourceEndpoint = cmd.apsFrame.destinationEndpoint
        self._responseApsFrame.destinationEndpoint = cmd.apsFrame.sourceEndpoint
        self._responseApsFrame.options = self.EMBER_AF_DEFAULT_APS_OPTIONS
        if cmd.apsFrame.options & ezsp.EMBER_APS_OPTION_ENCRYPTION:
            self._responseApsFrame.options |= ezsp.EMBER_APS_OPTION_ENCRYPTION
        if cmd.interPanHeader == None:
            self._responseDestination = cmd.source
            self._responseType &= ~EmberAfClusterCommand.ZCL_UTIL_RESP_INTERPAN



    def sendDefaultResponse(self, cmd, status):
        if cmd.type != ezsp.EMBER_INCOMING_UNICAST:
            if cmd.type != ezsp.EMBER_INCOMING_UNICAST_REPLY:
                return ezsp.EMBER_SUCCESS
        frameControl = ord(cmd.buffer[0])
        if frameControl & zcl.ZCL_DISABLE_DEFAULT_RESPONSE_MASK:
            if status == zcl.EMBER_ZCL_STATUS_SUCCESS:
                return ezsp.EMBER_SUCCESS
        if cmd.commandId == zcl.ZCL_DEFAULT_RESPONSE_COMMAND_ID:
            return ezsp.EMBER_SUCCESS
        frameControl = zcl.ZCL_PROFILE_WIDE_COMMAND
        if cmd.direction == EmberAfClusterCommand.ZCL_DIRECTION_CLIENT_TO_SERVER:
            frameControl |= zcl.ZCL_FRAME_CONTROL_SERVER_TO_CLIENT
        else:
            frameControl |= zcl.ZCL_FRAME_CONTROL_CLIENT_TO_SERVER
        if cmd.mfgSpecific:
            self._responseData = struct.pack('<BHBBBB', frameControl | zcl.ZCL_MANUFACTURER_SPECIFIC_MASK, cmd.mfgCode, cmd.seqNum, zcl.ZCL_DEFAULT_RESPONSE_COMMAND_ID, cmd.commandId, status)
        else:
            self._responseData = struct.pack('<BBBBB', frameControl & ~zcl.ZCL_MANUFACTURER_SPECIFIC_MASK, cmd.seqNum, zcl.ZCL_DEFAULT_RESPONSE_COMMAND_ID, cmd.commandId, status)
        self._prepareForResponse(cmd)
        self._sendResponse()



    def _processGlobalCommand(self, cmd):
        if cmd.commandId == zcl.ZCL_DEFAULT_RESPONSE_COMMAND_ID:
            (commandId, status,) = struct.unpack_from('<BB', cmd.buffer, cmd.payloadStartIndex)
            self.callback_afDefaultResponse(cmd.apsFrame.clusterId, commandId, status)



    def _processClusterSpecificCommand(self, cmd):
        status = self._clusterSpecificCommandParse(cmd)
        if status != zcl.EMBER_ZCL_STATUS_SUCCESS:
            self.sendDefaultResponse(cmd, status)
        return True



    def _processZdo(self, sender, apsFrame, message):
        if apsFrame.profileId != ezsp.EMBER_ZDO_PROFILE_ID:
            return False
        return self._nmProcessIncoming(sender, apsFrame, message)



    def _processMessage(self, apsFrame, type, message, source, interPanHeader):
        cmd = EmberAfClusterCommand()
        msgHandled = False
        cmd.apsFrame = apsFrame
        cmd.type = type
        cmd.source = source
        cmd.buffer = message
        cmd.clusterSpecific = False
        cmd.mfgSpecific = False
        cmd.direction = EmberAfClusterCommand.ZCL_DIRECTION_CLIENT_TO_SERVER
        cmd.payloadStartIndex = 1
        if len(message) < zcl.EMBER_AF_ZCL_OVERHEAD:
            return False
        frameControl = ord(message[0])
        if frameControl & int(zcl.ZCL_CLUSTER_SPECIFIC_COMMAND):
            cmd.clusterSpecific = True
        if frameControl & zcl.ZCL_MANUFACTURER_SPECIFIC_MASK:
            cmd.mfgSpecific = True
        if frameControl & zcl.ZCL_FRAME_CONTROL_DIRECTION_MASK:
            cmd.direction = EmberAfClusterCommand.ZCL_DIRECTION_SERVER_TO_CLIENT
        if cmd.mfgSpecific:
            if len(message) < zcl.EMBER_AF_ZCL_MANUFACTURER_SPECIFIC_OVERHEAD:
                return False
        if cmd.mfgSpecific:
            (cmd.mfgCode,) = struct.unpack_from('>H', message, cmd.payloadStartIndex)
            cmd.payloadStartIndex += 2
        else:
            cmd.mfgCode = 0
        cmd.seqNum = ord(message[cmd.payloadStartIndex])
        cmd.payloadStartIndex += 1
        cmd.commandId = ord(message[cmd.payloadStartIndex])
        cmd.payloadStartIndex += 1
        cmd.interPanHeader = interPanHeader
        self._currentCommand = cmd
        self._incomingZclSequenceNumber = cmd.seqNum
        self._prepareForResponse(cmd)
        if cmd.apsFrame.destinationEndpoint == ezsp.EMBER_BROADCAST_ENDPOINT:
            self.logger.warning('TODO: Broadcast message')
        elif cmd.clusterSpecific:
            msgHandled = self._processClusterSpecificCommand(cmd)
        else:
            msgHandled = self._processGlobalCommand(cmd)
        self._currentCommand = None
        return msgHandled



    def _incomingMessage(self, type, apsFrame, lastHopLqi, lastHopRssi, sender, bindingIndex, addressIndex, message):
        self._incomingMessagePacketStatsList.append(packet_statistics.PacketStatistics(sender, lastHopLqi, lastHopRssi))
        if self.EMBER_AF_ENABLE_FRAGMENTATION:
            if apsFrame.options & ezsp.EMBER_APS_OPTION_FRAGMENT:
                message = self.fragmentationIncomingMessage(apsFrame, sender, message)
                if not message:
                    return 
        self.currentMessagePacketStatsList = self._incomingMessagePacketStatsList
        self._incomingMessagePacketStatsList = []
        if self._serviceDiscoveryIncoming(sender, apsFrame, message):
            return 
        if self._processZdo(sender, apsFrame, message):
            return 
        if len(message) < zcl.EMBER_AF_ZCL_OVERHEAD:
            self.logger.error('Error: RX Packet too short')
            return 
        if self._processMessage(apsFrame, type, message, sender, None):
            return 


    _ncpNeedsResetAndInit = False

    def callback_unhandledCallback(self, callback):
        self.logger.warning('Unhandled callback 0x%02x' % callback)



    def callback_ezspErrorHandler(self, status):
        self.logger.error('Error: ezspErrorhandler 0x%02x' % status)
        self._ncpNeedsResetAndInit = True
        ezsp.EZSPInterface.callback_ezspErrorHandler(self, status)


    _currentSenderEui64 = None

    def callback_ezspIncomingSenderEui64Handler(self, senderEui64):
        self._currentSenderEui64 = senderEui64
        ezsp.EZSPInterface.callback_ezspIncomingSenderEui64Handler(self, senderEui64)



    def callback_ezspIncomingMessageHandler(self, type, apsFrame, lastHopLqi, lastHopRssi, sender, bindingIndex, addressIndex, message):
        self._incomingMessage(type, apsFrame, lastHopLqi, lastHopRssi, sender, bindingIndex, addressIndex, message)
        self._currentSenderEui64 = None
        ezsp.EZSPInterface.callback_ezspIncomingMessageHandler(self, type, apsFrame, lastHopLqi, lastHopRssi, sender, bindingIndex, addressIndex, message)



    def _stackStatusHandler(self, status):
        self._TCStackStatusHandler(status)
        if self.callback_afStackStatus(status):
            return 
        if status == ezsp.EMBER_NETWORK_UP or status == ezsp.EMBER_TRUST_CENTER_EUI_HAS_CHANGED:
            self.logger.info('EMBER_NETWORK_UP')
            if status == ezsp.EMBER_TRUST_CENTER_EUI_HAS_CHANGED:
                self.logger.info('Trust Center EUI has changed.')
                self.callback_afRegistrationAbort()
            self.callback_afRegistrationStart()
            try:
                if self.bridge_configuration['network_permit_joining']:
                    self.logger.info('Setting pjoin(255)')
                    self.emberPermitJoining(255)
            except KeyError:
                pass
        elif status == ezsp.EMBER_CHANNEL_CHANGED:
            self.logger.info('EMBER_CHANNEL_CHANGED')
        elif status == ezsp.EMBER_RECEIVED_KEY_IN_THE_CLEAR or status == ezsp.EMBER_NO_NETWORK_KEY_RECEIVED or status == ezsp.EMBER_PRECONFIGURED_KEY_REQUIRED or status == ezsp.EMBER_MOVE_FAILED or status == ezsp.EMBER_JOIN_FAILED or status == ezsp.EMBER_NETWORK_DOWN:
            if status == ezsp.EMBER_NETWORK_DOWN:
                self.logger.info('EMBER_NETWORK_DOWN')
            else:
                self.logger.warning('EMBER_JOIN_FAILED')
            if status == ezsp.EMBER_NETWORK_DOWN:
                pass
        else:
            self.logger.error('Unhandled stack status 0x%02x' % status)



    def callback_ezspStackStatusHandler(self, status):
        self._stackStatusHandler(status)
        ezsp.EZSPInterface.callback_ezspStackStatusHandler(self, status)



    def callback_ezspMessageSentHandler(self, type, indexOrDestination, apsFrame, messageTag, status, message):
        completed = True
        if self.EMBER_AF_ENABLE_FRAGMENTATION:
            if self._fragmentationMessageSent(apsFrame, status, messageTag):
                completed = False
        if completed:
            self.callback_afMessageSentHandler(type, indexOrDestination, apsFrame, status, message)
        ezsp.EZSPInterface.callback_ezspMessageSentHandler(self, type, indexOrDestination, apsFrame, messageTag, status, message)



    def callback_ezspChildJoinHandler(self, index, joining, childID, childEui64, childType):
        if joining:
            self.logger.debug('Node 0x%04x (%s) joined the network.' % (childID, byte_tuple.eui64ToHexString(childEui64)))
        else:
            self.logger.debug('Node 0x%04x (%s) left the network.' % (childID, byte_tuple.eui64ToHexString(childEui64)))
        ezsp.EZSPInterface.callback_ezspChildJoinHandler(self, index, joining, childID, childEui64, childType)



    def callback_ezspTimerHandler(self, timerId):
        if timerId == 0:
            self._TCTimer0Tick()
        elif timerId == 1:
            self.callback_afTimer1Handler()



    def callback_afStackStatus(self, status):
        return False



    def callback_afRegistrationAbort(self):
        pass



    def callback_afRegistrationStart(self):
        pass



    def callback_afTunnelingServerTunnelOpened(self, tunnelId, protocolId, manufacturerCode):
        pass



    def callback_afTunnelingServerDataReceived(self, tunnelId, data):
        pass



    def callback_afDefaultResponse(self, clusterId, commandId, status):
        pass



    def callback_afMessageSentHandler(self, type, indexOrDestination, apsFrame, status, message):
        pass



    def callback_afFragmentationMessageSentHandler(self, type, indexOrDestination, apsFrame, message, status):
        pass



    def callback_afTimer1Handler(self):
        pass



    def getNetworkInformationDict(self):
        networkStatusDict = {ezsp.EMBER_NO_NETWORK: 'EMBER_NO_NETWORK',
         ezsp.EMBER_JOINING_NETWORK: 'EMBER_JOINING_NETWORK',
         ezsp.EMBER_JOINED_NETWORK: 'EMBER_JOINED_NETWORK',
         ezsp.EMBER_JOINED_NETWORK_NO_PARENT: 'EMBER_JOINED_NETWORK_NO_PARENT',
         ezsp.EMBER_LEAVING_NETWORK: 'EMBER_LEAVING_NETWORK'}
        securityProfileDict = {security_config.NONE_SECURITY_PROFILE: 'No Security',
         security_config.HA_SECURITY_PROFILE: 'HA',
         security_config.SE_SECURITY_PROFILE_TEST: 'SE Test',
         security_config.SE_SECURITY_PROFILE_FULL: 'SE Full'}
        nodeTypeDict = {ezsp.EMBER_UNKNOWN_DEVICE: 'EMBER_UNKNOWN_DEVICE',
         ezsp.EMBER_COORDINATOR: 'EMBER_COORDINATOR',
         ezsp.EMBER_ROUTER: 'EMBER_ROUTER',
         ezsp.EMBER_END_DEVICE: 'EMBER_END_DEVICE',
         ezsp.EMBER_SLEEPY_END_DEVICE: 'EMBER_SLEEPY_END_DEVICE',
         ezsp.EMBER_MOBILE_END_DEVICE: 'EMBER_MOBILE_END_DEVICE'}
        powerModeDict = {ezsp.EMBER_TX_POWER_MODE_DEFAULT: 'EMBER_TX_POWER_MODE_DEFAULT',
         ezsp.EMBER_TX_POWER_MODE_BOOST: 'EMBER_TX_POWER_MODE_BOOST',
         ezsp.EMBER_TX_POWER_MODE_ALTERNATE: 'EMBER_TX_POWER_MODE_ALTERNATE',
         ezsp.EMBER_TX_POWER_MODE_BOOST_AND_ALTERNATE: 'EMBER_TX_POWER_MODE_BOOST_AND_ALTERNATE'}
        return_dict = {}
        state = self.emberNetworkState()
        return_dict['node_eui64'] = byte_tuple.eui64ToHexString(self._eui64)
        return_dict['network_status'] = networkStatusDict[state]
        power_mode_value = self.ezspGetConfigurationValue(ezsp.EZSP_CONFIG_TX_POWER_MODE)
        return_dict['radio_power_mode'] = powerModeDict[power_mode_value]
        if state == ezsp.EMBER_JOINED_NETWORK or state == ezsp.EMBER_JOINED_NETWORK_NO_PARENT:
            parameters = ezsp.EmberNetworkParameters()
            node = self.ezspGetNetworkParameters(parameters)
            if node in nodeTypeDict:
                nodeType = nodeTypeDict[node]
            else:
                nodeType = 'Unknown'
            securityLevel = self.ezspGetConfigurationValue(ezsp.EZSP_CONFIG_SECURITY_LEVEL)
            if self.EMBER_AF_SECURITY_PROFILE == security_config.CUSTOM_SECURITY_PROFILE:
                securityProfile = self.CUSTOM_PROFILE_STRING
            else:
                securityProfile = securityProfileDict[self.EMBER_AF_SECURITY_PROFILE]
            return_dict['node_type'] = nodeType
            return_dict['pan_id'] = '0x%04X' % parameters.panId
            return_dict['extended_pan_id'] = byte_tuple.extPanToHexString(parameters.extendedPanId)
            return_dict['node_id'] = '0x%04X' % self.emberGetNodeId()
            return_dict['channel'] = parameters.radioChannel
            return_dict['power'] = parameters.radioTxPower
            return_dict['security_level'] = securityLevel
            return_dict['security_profile'] = securityProfile
        return return_dict



    def getNetworkInformation(self):
        lines = []
        d = self.getNetworkInformationDict()
        lines.append('Node EUI64: %s' % d['node_eui64'])
        lines.append('Network state: %s' % d['network_status'])
        lines.append('Radio power mode: %s' % d['radio_power_mode'])
        if d.has_key('node_type'):
            lines.append('Node Type: %s' % d['node_type'])
            lines.append('PanID: %s ExtPanID: %s' % (d['pan_id'], d['extended_pan_id']))
            lines.append('NodeID: %s Channel: %i Power: %i' % (d['node_id'], d['channel'], d['power']))
            lines.append('Security level: %s Security profile: %s' % (d['security_level'], d['security_profile']))
        return lines



    def getRouteTableInformationArray(self):
        lines = []
        routeStatusDict = {0: 'Active',
         1: 'Discov',
         3: 'Unused'}
        concentratorTypeDict = {0: 'NotConc',
         1: 'LowRAM ',
         2: 'HighRAM'}
        routeRecordStateDict = {0: 'NoLongerNeeded',
         1: 'HasBeenSent',
         2: 'IsNeeded'}
        routeTableSize = 0
        routeTableSize = self.ezspGetConfigurationValue(ezsp.EZSP_CONFIG_ROUTE_TABLE_SIZE)
        lines.append('Route table:')
        lines.append('Indx Dest   NxtHop Status Age    ConType RouteRecState')
        i = 0
        entry = ezsp.EmberRouteTableEntry()
        while i < routeTableSize:
            self.emberGetRouteTableEntry(i, entry)
            lines.append('0x%02x 0x%04x 0x%04x %s %3iSec %s %s\n' % (i,
             entry.destination,
             entry.nextHop,
             routeStatusDict[entry.status],
             entry.age,
             concentratorTypeDict[entry.concentratorType],
             routeRecordStateDict[entry.routeRecordState]))
            i += 1

        return lines



    def getNeighborTableInformationString(self):
        neighborTableSize = self.emberNeighborCount()
        s = 'Neighbor table:\n'
        if neighborTableSize == 0:
            s += 'Empty\n'
            return s
        s += 'Indx ShortID AvLQI InCost OutCost Age\n'
        i = 0
        entry = ezsp.EmberNeighborTableEntry()
        while i < neighborTableSize:
            self.emberGetNeighbor(i, entry)
            s += '0x%02x 0x%04x  0x%02x  0x%02x   ' % (i,
             entry.shortId,
             entry.averageLqi,
             entry.inCost)
            s += '0x%02x  ' % entry.outCost
            s += '%3i\n' % entry.age
            i += 1

        return s



    def getChildTableInformationString(self):
        childTypeDict = {ezsp.EMBER_UNKNOWN_DEVICE: 'Unknown',
         ezsp.EMBER_COORDINATOR: 'Coordinator',
         ezsp.EMBER_ROUTER: 'Router',
         ezsp.EMBER_END_DEVICE: 'End device',
         ezsp.EMBER_SLEEPY_END_DEVICE: 'Sleepy end device',
         ezsp.EMBER_MOBILE_END_DEVICE: 'Mobile end device '}
        (childTableSize, parentEui64, parentNodeId,) = self.ezspGetParentChildParameters()
        s = "This node's parent (if applicable):\n"
        s += '0x%04x (%s)\n\n' % (parentNodeId, byte_tuple.eui64ToHexString(parentEui64))
        s += 'Child table:\n'
        if childTableSize == 0:
            s += 'Empty\n'
            return s
        s += 'Indx ShortID LongID             Type\n'
        i = 0
        while i < childTableSize:
            try:
                (childId, childEui64, childType,) = self.ezspGetChildData(i)
            except ezsp.EmberStatus as e:
                if e.value == ezsp.EMBER_NOT_JOINED:
                    s += '0x%02x EMBER_NOT_JOINED\n' % i
                else:
                    raise 
            else:
                s += '0x%02x 0x%04x  %s %s\n' % (i,
                 childId,
                 byte_tuple.eui64ToHexString(childEui64),
                 childTypeDict[childType])
            i += 1

        return s



    def getAddressTableInformationString(self):
        s = 'Address table:\n'
        if self.EMBER_AF_ADDRESS_TABLE_SIZE == 0:
            s += 'Empty\n'
            return s
        s += 'Indx NodeID EUI64\n'
        i = 0
        while i < self.EMBER_AF_ADDRESS_TABLE_SIZE:
            NodeId = self.emberGetAddressTableRemoteNodeId(i)
            s += '0x%02x ' % i
            if NodeId == ezsp.EMBER_TABLE_ENTRY_UNUSED_NODE_ID:
                s += 'Unused\n'
            else:
                Eui64 = self.emberGetAddressTableRemoteEui64(i)
                s += '0x%04x %s\n' % (NodeId, byte_tuple.eui64ToHexString(Eui64))
            i += 1

        return s



    def getAddressTableInformationArray(self):
        address_table = []
        i = 0
        while i < self.EMBER_AF_ADDRESS_TABLE_SIZE:
            address_info = {}
            address_info['index'] = '0x%02x ' % i
            NodeId = self.emberGetAddressTableRemoteNodeId(i)
            if NodeId != ezsp.EMBER_TABLE_ENTRY_UNUSED_NODE_ID:
                Eui64 = self.emberGetAddressTableRemoteEui64(i)
                address_info['nodeId'] = '0x%04x' % NodeId
                address_info['eui64'] = byte_tuple.eui64ToHexString(Eui64)
            address_table.append(address_info)
            i += 1

        return address_table



    def getChildTableInformationArray(self):
        childTypeDict = {ezsp.EMBER_UNKNOWN_DEVICE: 'Unknown',
         ezsp.EMBER_COORDINATOR: 'Coordinator',
         ezsp.EMBER_ROUTER: 'Router',
         ezsp.EMBER_END_DEVICE: 'End device',
         ezsp.EMBER_SLEEPY_END_DEVICE: 'Sleepy end device',
         ezsp.EMBER_MOBILE_END_DEVICE: 'Mobile end device '}
        children = []
        (childTableSize, parentEui64, parentNodeId,) = self.ezspGetParentChildParameters()
        i = 0
        while i < childTableSize:
            (childId, childEui64, childType,) = self.ezspGetChildData(i)
            child_data = {'eui64': byte_tuple.eui64ToHexString(childEui64, False),
             'childType': childTypeDict[childType],
             'nodeId': self.emberLookupNodeIdByEui64(childEui64)}
            children.append(child_data)
            i += 1

        return children



    def getStackVersionString(self):
        (ncpEzspProtocolVersion, ncpStackType, ncpStackVersion,) = self.ezspVersion(ezsp_protocol.EZSP_PROTOCOL_VERSION)
        s = '0x%04X\n' % ncpStackVersion
        return s



    def getHostEui64(self):
        return self._eui64




+++ okay decompyling ./framework.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2016.01.27 00:42:49 MSK
