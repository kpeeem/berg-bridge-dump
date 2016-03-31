# 2016.01.27 00:42:44 MSK
import ezsp
import random
FORM_AND_JOIN_NOT_SCANNING = 0
FORM_AND_JOIN_NEXT_NETWORK = 1
FORM_AND_JOIN_ENERGY_SCAN = 2
FORM_AND_JOIN_PAN_ID_SCAN = 3
FORM_AND_JOIN_JOINABLE_SCAN = 4
DEBUG_ENERGY_SCAN = 5
ALL_CHANNEL_LIST = [ a for a in range(11, 27) ]
ENERGY_SCAN_DURATION = 5
ACTIVE_SCAN_DURATION = 3
MAX_PANID_ATTEMPTS = 100
ENERGY_BAND = 10

class FormAndJoin:
    _scanType = FORM_AND_JOIN_NOT_SCANNING

    def channelListToMask(self, channelList):
        mask = 0
        for c in channelList:
            mask |= 1 << c

        return mask



    def scanForUnusedPanId(self, channelList = ALL_CHANNEL_LIST, duration = ENERGY_SCAN_DURATION):
        if not self._setup(FORM_AND_JOIN_ENERGY_SCAN):
            return False
        self._channelEnergies = []
        self._startScan(ezsp.EMBER_ENERGY_SCAN, self.channelListToMask(channelList), duration)
        return True



    def debugEnergyScan(self, channelList = ALL_CHANNEL_LIST, duration = 1):
        if self._scanType != FORM_AND_JOIN_NOT_SCANNING:
            return False
        self._scanType = DEBUG_ENERGY_SCAN
        self._channelEnergies = []
        self._startScan(ezsp.EMBER_ENERGY_SCAN, self.channelListToMask(channelList), duration)
        return True



    def _debugEnergyScanComplete(self):
        self.callback_debugEnergyScanCompleteHandler(self._channelEnergies)
        self._cleanup(ezsp.EMBER_SUCCESS)



    def _energyScanComplete(self):
        self._channelEnergies.sort(key=lambda n: n[1])
        lowestEnergy = self._channelEnergies[0][1]
        candidates = []
        for c in self._channelEnergies:
            if c[1] < lowestEnergy + ENERGY_BAND:
                candidates.append(c)

        self._channel = random.choice(candidates)[0]
        self._startPanIdScan()



    def _startPanIdScan(self):
        self._networks = []
        self._scanType = FORM_AND_JOIN_PAN_ID_SCAN
        self._startScan(ezsp.EMBER_ACTIVE_SCAN, 1 << self._channel, ACTIVE_SCAN_DURATION)



    def _panIdScanComplete(self):
        attempt = 0
        while attempt < MAX_PANID_ATTEMPTS:
            panId = random.randint(0, 65535)
            duplicate = False
            for n in self._networks:
                if n[0].panId == panId:
                    duplicate = True

            if not duplicate:
                self._cleanup(ezsp.EMBER_SUCCESS)
                self.callback_afUnusedPanIdFoundHandler(panId, self._channel)
                return 
            attempt += 1

        self._cleanup(ezsp.EMBER_ERR_FATAL)



    def scanForJoinableNetwork(self, channelList = ALL_CHANNEL_LIST, extendedPanId = None):
        if not self._setup(FORM_AND_JOIN_NEXT_NETWORK):
            return ezsp.EMBER_INVALID_CALL
        self._channelList = channelList
        self._networks = []
        self._extendedPanId = extendedPanId
        return self.scanForNextJoinableNetwork()



    def scanForNextJoinableNetwork(self):
        if self._scanType != FORM_AND_JOIN_NEXT_NETWORK:
            self.callback_afScanErrorHandler(ezsp.EMBER_INVALID_CALL)
            return ezsp.EMBER_INVALID_CALL
        while len(self._networks) > 0:
            candidate = self._networks.pop()
            if candidate[0].allowingJoin and candidate[0].stackProfile == self._stackProfile and (self._extendedPanId == None or candidate[0].extendedPanId == self._extendedPanId):
                self.callback_afJoinableNetworkFoundHandler(candidate[0], candidate[1], candidate[2])
                return ezsp.EMBER_SUCCESS

        if len(self._channelList) > 0:
            self._scanType = FORM_AND_JOIN_JOINABLE_SCAN
            self._startScan(ezsp.EMBER_ACTIVE_SCAN, 1 << self._channelList.pop(), ACTIVE_SCAN_DURATION)
        else:
            self._cleanup(ezsp.EMBER_NO_BEACONS)
        return ezsp.EMBER_SUCCESS



    def callback_ezspScanCompleteHandler(self, channel, status):
        if self._scanType == FORM_AND_JOIN_ENERGY_SCAN:
            self._energyScanComplete()
        elif self._scanType == DEBUG_ENERGY_SCAN:
            self._debugEnergyScanComplete()
        elif self._scanType == FORM_AND_JOIN_PAN_ID_SCAN:
            self._panIdScanComplete()
        elif self._scanType == FORM_AND_JOIN_JOINABLE_SCAN:
            self._scanType = FORM_AND_JOIN_NEXT_NETWORK
            self.scanForNextJoinableNetwork()
        ezsp.EZSPInterface.callback_ezspScanCompleteHandler(self, channel, status)



    def callback_ezspNetworkFoundHandler(self, networkFound, lqi, rssi):
        if self._scanType == FORM_AND_JOIN_PAN_ID_SCAN or self._scanType == FORM_AND_JOIN_JOINABLE_SCAN:
            self._networks.append((networkFound, lqi, rssi))
        ezsp.EZSPInterface.callback_ezspNetworkFoundHandler(self, networkFound, lqi, rssi)



    def callback_ezspEnergyScanResultHandler(self, channel, maxRssiValue):
        self._channelEnergies.append((channel, maxRssiValue))
        ezsp.EZSPInterface.callback_ezspEnergyScanResultHandler(self, channel, maxRssiValue)



    def callback_afUnusedPanIdFoundHandler(self, panId, channel):
        pass



    def callback_afJoinableNetworkFoundHandler(self, network, lqi, rssi):
        pass



    def callback_afScanErrorHandler(self, status):
        pass



    def callback_debugEnergyScanCompleteHandler(self, result):
        print '\nCh  RSSI dBm'
        for ch in result:
            print '%i  %i' % (ch[0], ch[1])




    def _isScanning(self):
        if self._scanType == FORM_AND_JOIN_NOT_SCANNING:
            return False
        if self._scanType == FORM_AND_JOIN_NEXT_NETWORK:
            return False
        return True



    def _setup(self, scanType):
        if self._isScanning():
            self.callback_afScanErrorHandler(ezsp.EMBER_MAC_SCANNING)
            return False
        self._scanType = scanType
        return True



    def _cleanup(self, status):
        self._scanType = FORM_AND_JOIN_NOT_SCANNING
        if status != ezsp.EMBER_SUCCESS:
            self.callback_afScanErrorHandler(status)



    def _startScan(self, type, mask, duration):
        status = ezsp.EMBER_SUCCESS
        try:
            self.emberStartScan(type, mask, duration)
        except ezsp.EmberStatus as e:
            status = e.value
        if status != ezsp.EMBER_SUCCESS:
            self._cleanup(status)




+++ okay decompyling ./form_and_join.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2016.01.27 00:42:45 MSK
