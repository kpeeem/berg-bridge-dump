# 2016.01.27 00:42:31 MSK
import os
import time
import threading
import thread
import struct
import Queue
import signal
import sys
import ezsp
import framework
import config
import security_config
import zcl
import byte_tuple
import bridge_event
import device_event
import device_command
import customlogger
PROFILE_ID = 49152
MANUFACTURER_ID = 4098
WEMINUCHE_CLUSTER_ID = 65280
SOURCE_ENDPOINT = 1
DESTINATION_ENDPOINT = 1
APP_MAX_WRITE_ATTEMPTS = 4
APP_RETRY_DELAY = 1.0

class WeminucheApi(framework.ApplicationFramework):
    EMBER_APPLICATION_RECEIVES_SUPPORTED_ZDO_REQUESTS = False
    EMBER_APPLICATION_HANDLES_UNSUPPORTED_ZDO_REQUESTS = False
    EMBER_APPLICATION_HANDLES_ENDPOINT_ZDO_REQUESTS = False
    EMBER_APPLICATION_HANDLES_BINDING_ZDO_REQUESTS = False
    EMBER_SOURCE_ROUTE_TABLE_SIZE = 0
    EMBER_AF_ADDRESS_TABLE_SIZE = 8
    EMBER_AF_TRUST_CENTER_ADDRESS_CACHE_SIZE = 2
    EMBER_KEY_TABLE_SIZE = 16
    EMBER_AF_MANUFACTURER_CODE = 43690
    EMBER_AF_ENABLE_FRAGMENTATION = True
    EMBER_AF_FRAGMENT_BUFFER_SIZE = 1024
    EMBER_AF_FRAGMENTATION_MAXIMUM_RECEIVED_FRAGMENTS = 30
    EMBER_END_DEVICE_POLL_TIMEOUT = 1
    EMBER_END_DEVICE_POLL_TIMEOUT_SHIFT = 6
    ZA_DEVICE_TYPE = config.ZA_COORDINATOR
    EMBER_AF_CONCENTRATOR = False
    EMBER_STACK_PROFILE = 2
    EMBER_AF_SECURITY_PROFILE = security_config.CUSTOM_SECURITY_PROFILE
    CUSTOM_PROFILE_STRING = 'Custom'
    _EP1 = {'endpoint_number': 1,
     'profile_id': 49152,
     'device_id': 1,
     'device_version': 0,
     'in_clusters': [0, 65280],
     'out_clusters': [0, 65280]}
    ENDPOINTS = [_EP1]
    DEFAULT_BRIDGE_CONFIGURATION = {'extended_pan_id': 4775313444792434688L,
     'radio_power': 8,
     'tx_power_mode': ezsp.EMBER_TX_POWER_MODE_BOOST,
     'channel_list': [11,
                      14,
                      15,
                      19,
                      20,
                      24,
                      25],
     'network_create': False,
     'network_permit_joining': False,
     'print_progress_dots': True,
     'purge_link_keys': False,
     'disable_relay': 1}
    CALLBACK_RATE_TIME = 0.03

    def __init__(self, event_queue, bridge_configuration = None):
        self.logger = customlogger.Logger('api')
        self.event_queue = event_queue
        self.watchdog_delegate = None
        self.telemetry_delegate = None
        if type(bridge_configuration) == type(dict()):
            self.bridge_configuration = dict(WeminucheApi.DEFAULT_BRIDGE_CONFIGURATION.items() + bridge_configuration.items())
        else:
            self.bridge_configuration = default_bridge_configuration
        super(WeminucheApi, self).__init__()
        self.init()
        self.logger.info('Finished NCP init()')
        self._pending_response = threading.Event()
        self._pending_sent = threading.Event()
        self.callbackThread_run = threading.Event()
        self.callbackThread = threading.Thread(target=self._callbacks)
        self.callbackThread.start()
        try:
            if self.bridge_configuration['purge_link_keys']:
                self.logger.info('Removing all link keys')
                self.TCDeleteAllKeys()
            if not self._joinedNetwork:
                if self.bridge_configuration['network_create']:
                    self.logger.info('Attempting to create PAN on channels %s' % self.bridge_configuration['channel_list'])
                    self.scanForUnusedPanId(self.bridge_configuration['channel_list'])
        except KeyError:
            pass



    def shutdown(self):
        while self.callbackThread.isAlive():
            self.callbackThread_run.set()




    def _callbacks(self):
        callbackRateLimiter = threading.Condition()
        while self.callbackThread_run.isSet() == False:
            try:
                if self.watchdog_delegate:
                    self.watchdog_delegate.updateKey('callbackThread')
                callback = self.ezspCallback()
                self.dispatchCallback(callback)
                if callback == ezsp.EZSP_NO_CALLBACKS:
                    callbackRateLimiter.acquire()
                    callbackRateLimiter.wait(self.CALLBACK_RATE_TIME)
            except:
                self.logger.exception('Unexpected callback thread error:', sys.exc_info())
                signal.alarm(1)
                break

        self.logger.warning('callbackThread has finished')



    def _blockingWrite(self, nodeId, data):
        attempt = 1
        if self.bridge_configuration['print_progress_dots']:
            print '.',
        while attempt <= APP_MAX_WRITE_ATTEMPTS:
            self._pending_response.clear()
            self._pending_sent.clear()
            self._sendResult = device_command.RSP_FAILED_NETWORK
            frameControl = zcl.ZCL_CLUSTER_SPECIFIC_COMMAND | zcl.ZCL_FRAME_CONTROL_CLIENT_TO_SERVER | 4
            sequence = self._incomingZclSequenceNumber
            commandId = 1
            message = struct.pack('<BHBB', frameControl, MANUFACTURER_ID, sequence, commandId) + data
            apsFrame = ezsp.EmberApsFrame()
            apsFrame.profileId = PROFILE_ID
            apsFrame.clusterId = WEMINUCHE_CLUSTER_ID
            apsFrame.sourceEndpoint = SOURCE_ENDPOINT
            apsFrame.destinationEndpoint = DESTINATION_ENDPOINT
            apsFrame.options = self.EMBER_AF_DEFAULT_APS_OPTIONS
            try:
                self.sendUnicast(ezsp.EMBER_OUTGOING_DIRECT, nodeId, apsFrame, message)
            except ezsp.EmberStatus as e:
                if e.value == ezsp.EMBER_DELIVERY_FAILED:
                    self.logger.debug('sendUnicast delivery failed.')
                else:
                    raise 
            self._pending_sent.wait(5)
            if self._pending_sent.isSet():
                self._pending_response.wait(5)
                if self._pending_response.isSet():
                    if self._sendResult == device_command.RSP_SUCCESS:
                        return self._sendResult
                    self.logger.warning('Received error result from device, code 0x%02x' % self._sendResult)
                else:
                    self.logger.warning('Timed out waiting for response from device.')
            else:
                self.logger.warning('Timed out waiting for messageSent callbacks.')
                self.fragmentationCancelSendUnicast()
            attempt += 1
            if attempt <= APP_MAX_WRITE_ATTEMPTS:
                self.logger.warning('Retrying. Attempt %i of %i.' % (attempt, APP_MAX_WRITE_ATTEMPTS))
                time.sleep(APP_RETRY_DELAY)

        return self._sendResult



    def executeCommand(self, command):
        nodeId = self.emberLookupNodeIdByEui64(command.device_address)
        if nodeId == 0:
            return device_command.RSP_EUI64_NOT_FOUND
        infile = command.payload
        sending = True
        blockID = 0
        length = command.payload_length
        if self.telemetry_delegate:
            self.telemetry_delegate.commandTransferStarted(byte_tuple.eui64ToHexString(command.device_address), length)
        while sending:
            self.logger.debug('Command progress: %d bytes remaining' % max(length, 0))
            if self.watchdog_delegate:
                self.watchdog_delegate.updateKey('commandThread')
            fileData = infile.read(512)
            if len(fileData) != 0:
                data = struct.pack('>B', blockID)
                data += fileData
                blockID += 1
                if blockID > 255:
                    blockID = 1
                try:
                    result = self._blockingWrite(nodeId, data)
                except:
                    if self.telemetry_delegate:
                        self.telemetry_delegate.commandTransferEnded(False)
                    infile.close()
                    raise 
                if result != device_command.RSP_SUCCESS:
                    if self.telemetry_delegate:
                        self.telemetry_delegate.commandTransferEnded(False)
                    infile.close()
                    return result
            else:
                sending = False
            if self.telemetry_delegate:
                self.telemetry_delegate.incrementCommandBytesTransferred(512)
            length = length - 512

        if self.telemetry_delegate:
            self.telemetry_delegate.commandTransferEnded(True)
        infile.close()
        return device_command.RSP_SUCCESS



    def formNetwork(self, parameters):
        if self.ZA_DEVICE_TYPE != config.ZA_COORDINATOR:
            return False
        self.TCSecurityInit()
        self.logger.info('Forming network on channel %i, panID 0x%04x' % (parameters.radioChannel, parameters.panId))
        self.emberFormNetwork(parameters)
        return True



    def callback_afStackStatus(self, status):
        if status == ezsp.EMBER_NETWORK_UP or status == ezsp.EMBER_TRUST_CENTER_EUI_HAS_CHANGED:
            pass
        return False



    def _weminucheEventCallback(self, senderEui64, data, packetStatsList):
        if self.telemetry_delegate and senderEui64 != None:
            self.telemetry_delegate.packetsReceived(senderEui64, packetStatsList)
        event = device_event.DeviceEvent(self.getHostEui64(), senderEui64, data)
        try:
            self.event_queue.put(event, False)
        except Queue.Full:
            self.logger.warning('Received device event, but the event queue full')
        return True



    def _weminucheCommandResponseCallback(self, senderEui64, data, packetStatsList):
        if self.telemetry_delegate and senderEui64 != None:
            self.telemetry_delegate.packetsReceived(senderEui64, packetStatsList)
        self._sendResult = ord(data[10])
        self._pending_response.set()
        return True



    def _weminucheLinkKeyRequiredCallback(self, eui64):
        event_payload = {'name': 'encryption_key_required',
         'device_address': byte_tuple.eui64ToHexString(eui64, False)}
        event = bridge_event.BridgeEvent(self.getHostEui64(), event_payload)
        try:
            self.event_queue.put(event, False)
        except Queue.Full:
            self.logger.warning('Received bridge event, but the event queue full')
        self.logger.info('Link key required for %s' % byte_tuple.eui64ToHexString(eui64))
        return True



    def callback_afFragmentationMessageSentHandler(self, type, indexOrDestination, apsFrame, message, status):
        self._pending_sent.set()



    def callback_afMessageSentHandler(self, type, indexOrDestination, apsFrame, status, message):
        self._pending_sent.set()



    def callback_afUnusedPanIdFoundHandler(self, panId, channel):
        parameters = ezsp.EmberNetworkParameters()
        parameters.extendedPanId = byte_tuple.convertToExtPan(self.bridge_configuration['extended_pan_id'])
        parameters.panId = panId
        parameters.radioTxPower = self.bridge_configuration['radio_power']
        parameters.radioChannel = channel
        self.formNetwork(parameters)
        framework.ApplicationFramework.callback_afUnusedPanIdFoundHandler(self, panId, channel)



    def callback_afScanErrorHandler(self, status):
        self.logger.error('Scan error, status = 0x%02x' % status)
        framework.ApplicationFramework.callback_afScanErrorHandler(self, status)



    def setWatchdogDelegate(self, delegate):
        self.watchdog_delegate = delegate



    def setTelemetryDelegate(self, delegate):
        self.telemetry_delegate = delegate




+++ okay decompyling ./api.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2016.01.27 00:42:32 MSK
