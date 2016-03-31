# 2016.01.27 00:42:45 MSK
import ezsp
import util
import string
import ezsp_protocol
import threading
_MAX_INT8U_VALUE = 255
_FRAGMENTATION_MAXIMUM_RECEIVED_FRAGMENTS = 255

def HIGH_LOW_TO_INT(high, low):
    high = high & 255
    low = low & 255
    return high << 8 | low



def LOW_BYTE(n):
    return n & 255



def HIGH_BYTE(n):
    return n >> 8 & 255



class Fragmentation:
    _fragmentWindowSize = None
    _ackTimeout = None

    def fragmentationInit(self):
        self._ackTimeout = self.ezspGetConfigurationValue(ezsp.EZSP_CONFIG_APS_ACK_TIMEOUT)
        self._fragmentWindowSize = self.ezspGetConfigurationValue(ezsp.EZSP_CONFIG_FRAGMENT_WINDOW_SIZE)
        self._fragmentationLock = threading.RLock()


    _txMessageType = None
    _txIndexOrDestination = None
    _txApsFrame = None
    _txBuffer = None
    _txFragmentCount = None
    _txFragmentBase = None
    _txFragmentsInTransit = None

    def fragmentationCancelSendUnicast(self):
        with self._fragmentationLock:
            while self._txMessageType != None:
                self._fragmentationMessageSent(self._txApsFrame, ezsp.EMBER_ERR_FATAL, 255)




    def fragmentationSendUnicast(self, type, indexOrDestination, apsFrame, buffer):
        with self._fragmentationLock:
            if self._fragmentWindowSize == None:
                self.logger.error('fragmentationSendUnicast() returning EMBER_INVALID_CALL')
                return ezsp.EMBER_INVALID_CALL
            else:
                if self._txMessageType != None:
                    self.logger.error('fragmentationSendUnicast() returning EMBER_MAX_MESSAGE_LIMIT_REACHED')
                    return ezsp.EMBER_MAX_MESSAGE_LIMIT_REACHED
                self._txMessageType = type
                self._txIndexOrDestination = indexOrDestination
                self._txApsFrame = apsFrame
                self._txApsFrame.options |= ezsp.EMBER_APS_OPTION_FRAGMENT | ezsp.EMBER_APS_OPTION_RETRY
                self._txBuffer = buffer
                self._txFragmentLen = self.maximumApsPayloadLength(type, indexOrDestination, self._txApsFrame)
                fragments = (len(self._txBuffer) + self._txFragmentLen - 1) // self._txFragmentLen
                if fragments > _MAX_INT8U_VALUE:
                    return ezsp.EMBER_MESSAGE_TOO_LONG
                self._txFragmentCount = fragments
                self._txFragmentBase = 0
                self._txFragmentsInTransit = 0
                self._fragmentStatusList = []
                status = self._sendNextFragments()
                if status != ezsp.EMBER_SUCCESS:
                    self._txMessagetype = None
                return status



    def _sendNextFragments(self):
        with self._fragmentationLock:
            offset = self._txFragmentBase * self._txFragmentLen
            i = self._txFragmentBase
            while i < self._txFragmentBase + self._fragmentWindowSize and i < self._txFragmentCount:
                if offset + self._txFragmentLen < len(self._txBuffer):
                    fragmentLen = self._txFragmentLen
                else:
                    fragmentLen = len(self._txBuffer) - offset
                self._txApsFrame.groupId = HIGH_LOW_TO_INT(self._txFragmentCount, i)
                fragmentData = self._txBuffer[offset:(offset + fragmentLen)]
                try:
                    self._txApsFrame.sequence = self.ezspSendUnicast(self._txMessageType, self._txIndexOrDestination, self._txApsFrame, i, fragmentData)
                except:
                    self.fragmentationCancelSendUnicast()
                    raise 
                self._txFragmentsInTransit += 1
                offset += fragmentLen
                i += 1

            return ezsp.EMBER_SUCCESS



    def _fragmentationMessageSent(self, apsFrame, status, messageTag):
        with self._fragmentationLock:
            if apsFrame.options & ezsp.EMBER_APS_OPTION_FRAGMENT:
                if self._txApsFrame.sequence != apsFrame.sequence:
                    self.logger.info('Rxd block with sequence 0x%02x - expected 0x%02x - ignored.' % (apsFrame.sequence, self._txApsFrame.sequence))
                    return True
                self._fragmentStatusList.append((messageTag, status))
                if self._txFragmentsInTransit > 0:
                    self._txFragmentsInTransit -= 1
                if self._txFragmentsInTransit == 0:
                    self._txMessageType = None
                    status = ezsp.EMBER_SUCCESS
                    for a in self._fragmentStatusList:
                        if a[1] != ezsp.EMBER_SUCCESS:
                            status = ezsp.EMBER_ERR_FATAL

                    if status != ezsp.EMBER_SUCCESS:
                        self.logger.warning('Send failed, fragment status:')
                        for a in self._fragmentStatusList:
                            self.logger.warning('%i = 0x%08x' % (a[0], a[1]))

                        if self.telemetry_delegate:
                            self.telemetry_delegate.packetFailed()
                    self.callback_afFragmentationMessageSentHandler(self._txMessageType, self._txIndexOrDestination, self._txApsFrame, self._txBuffer, status)
                return True
            else:
                return False


    _rxFragmentSource = None
    _rxFragmentSequenceNumber = None
    _rxFragmentBase = 0
    _rxFragmentsReceived = None
    _rxFragmentsExpected = None

    def _lowBitMask(self, n):
        return (1 << n) - 1



    def _setFragmentMask(self):
        highestZeroBit = self._fragmentWindowSize
        if self._rxFragmentsExpected < self._rxFragmentBase + self._fragmentWindowSize:
            highestZeroBit = self._rxFragmentsExpected % self._fragmentWindowSize
        self._rxFragmentMask = ~self._lowBitMask(highestZeroBit)
        self._rxFragmentMask &= 255



    def fragmentationIncomingMessage(self, apsFrame, sender, buffer):
        if not apsFrame.options & ezsp.EMBER_APS_OPTION_FRAGMENT:
            return 
        fragment = LOW_BYTE(apsFrame.groupId)
        if self._rxFragmentSource == None and fragment < self._fragmentWindowSize:
            self._rxFragmentSource = sender
            self._rxFragmentSequenceNumber = apsFrame.sequence
            self._rxFragementBase = 0
            self._rxFragmentsReceived = 0
            self._rxFragmentsExpected = 255
            self._setFragmentMask()
            self._rxFragmentList = []
        if self._rxFragmentSource != sender or self._rxFragmentSequenceNumber != apsFrame.sequence:
            return 
        if self._rxFragmentMask == 255 and self._rxFragmentBase + self._fragmentWindowSize <= fragment:
            self._rxFragmentBase += self._fragmentWindowSize
            self._setFragmentMask()
        if self._rxFragmentBase + self._fragmentWindowSize <= fragment:
            return 
        mask = 1 << fragment % self._fragmentWindowSize
        newFragment = not mask & self._rxFragmentMask
        if fragment == 0:
            self._rxFragmentsExpected = HIGH_BYTE(apsFrame.groupId)
            if self._rxFragmentsExpected < self._fragmentWindowSize:
                self._setFragmentMask()
            if self._rxFragmentsExpected > _FRAGMENTATION_MAXIMUM_RECEIVED_FRAGMENTS:
                self._fragmentationAbortReception()
                return 
        self._rxFragmentMask |= mask
        if newFragment:
            self._rxFragmentsReceived += 1
            if not self._storeRxFragment(fragment, buffer):
                self._fragmentationAbortReception()
                return 
        if fragment == self._rxFragmentsExpected - 1 or self._rxFragmentMask | self._lowBitMask(fragment % self._fragmentWindowSize) == 255:
            apsFrame.groupId = HIGH_LOW_TO_INT(self._rxFragmentMask, self._rxFragmentBase)
            self.ezspSendReply(sender, apsFrame, '')
        if self._rxFragmentsReceived == self._rxFragmentsExpected:
            self._rxFragmentSource = None
            apsFrame.options &= ~ezsp.EMBER_APS_OPTION_RETRY
            buffer = string.join(self._rxFragmentList, '')
            return buffer



    def _fragmentationAbortReception(self):
        self._rxFragmentSource = None



    def _storeRxFragment(self, fragment, buffer):
        self._rxFragmentList.insert(fragment, buffer)
        return True




+++ okay decompyling ./fragmentation.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2016.01.27 00:42:46 MSK
