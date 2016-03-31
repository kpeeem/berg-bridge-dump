# 2016.01.27 00:42:58 MSK
import ezsp
import security_config
import customlogger
import byte_tuple
TC_LINK_KEY_REQUEST_POLICY = False
TC_APP_KEY_REQUEST_POLICY = False
TC_NETWORK_KEY_UPDATE_PERIOD_MINS = 60
TC_NWK_KEY_WAIT = 0
TC_NWK_KEY_UPDATE = 1
TC_NWK_KEY_SWITCH = 2

class TrustCenter:

    def _createRandomKey(self):
        i = 0
        keyBytes = []
        while i < ezsp.EMBER_ENCRYPTION_KEY_SIZE:
            n = int(self.ezspGetRandomNumber())
            keyBytes.append(n >> 8 & 255)
            keyBytes.append(n & 255)
            i += 2

        return tuple(keyBytes)



    def TCSecurityPolicyInit(self):
        self._permitRequestingTrustCenterLinkKey(TC_LINK_KEY_REQUEST_POLICY)
        self._permitRequestingApplicationLinkKey(TC_APP_KEY_REQUEST_POLICY)
        self._setEzspPolicy(ezsp.EZSP_TRUST_CENTER_POLICY, ezsp.EZSP_ALLOW_PRECONFIGURED_KEY_JOINS, 'TC Policy', 'EZSP_ALLOW_PRECONFIGURED_KEY_JOINS')



    def TCSecurityInit(self):
        securityState = ezsp.EmberInitialSecurityState()
        securityState.bitmask = 0
        securityState.preconfiguredKey = ezsp.EmberKeyData()
        securityState.preconfiguredKey.contents = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        securityState.networkKey = ezsp.EmberKeyData()
        securityState.networkKey.contents = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        securityState.nwkKeySequenceNumber = 0
        securityState.preconfiguredTrustCenterEui64 = (0, 0, 0, 0, 0, 0, 0, 0)
        if self.EMBER_AF_SECURITY_PROFILE == security_config.CUSTOM_SECURITY_PROFILE:
            securityState.bitmask = ezsp.EMBER_HAVE_NETWORK_KEY
            securityState.networkKey.contents = self._createRandomKey()
        self.emberSetInitialSecurityState(securityState)
        self.TCSecurityPolicyInit()



    def TCSecurityJoinNotify(self):
        pass



    def TCNetworkKeyUpdate(self):
        newKey = ezsp.EmberKeyData()
        newKey.contents = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        try:
            self.emberBroadcastNextNetworkKey(newKey)
        except ezsp.EmberStatus as e:
            if e.value == ezsp.EMBER_INVALID_CALL:
                self.logger.info('TC: emberBroadcastNextNetworkKey() returned EMBER_INVALID_CALL')
                return False
            raise 
        return True



    def TCNetworkKeySwitch(self):
        try:
            self.emberBroadcastNetworkKeySwitch()
        except ezsp.EmberStatus as e:
            if e.value == ezsp.EMBER_INVALID_CALL:
                self.logger.info('TC: emberBroadcastNetworkKeySwitch() returned EMBER_INVALID_CALL')
                return False
            if e.value == ezsp.EMBER_TOO_SOON_FOR_SWITCH_KEY:
                self.logger.info('TC: emberBroadcastNetworkKeySwitch() returned EMBER_TOO_SOON_FOR_SWITCH_KEY')
                return False
            raise 
        return True



    def _permitRequestingTrustCenterLinkKey(self, allow):
        if allow:
            self._setEzspPolicy(ezsp.EZSP_TC_KEY_REQUEST_POLICY, ezsp.EZSP_ALLOW_TC_KEY_REQUESTS, 'TC Key Request', 'Allow')
        else:
            self._setEzspPolicy(ezsp.EZSP_TC_KEY_REQUEST_POLICY, ezsp.EZSP_DENY_TC_KEY_REQUESTS, 'TC Key Request', 'Deny')



    def _permitRequestingApplicationLinkKey(self, allow):
        if allow:
            self._setEzspPolicy(ezsp.EZSP_APP_KEY_REQUEST_POLICY, ezsp.EZSP_ALLOW_APP_KEY_REQUESTS, 'App  Key Request', 'Allow')
        else:
            self._setEzspPolicy(ezsp.EZSP_APP_KEY_REQUEST_POLICY, ezsp.EZSP_DENY_APP_KEY_REQUESTS, 'App Key Request', 'Deny')



    def TCAddOrUpdateKey(self, address, key):
        keyData = ezsp.EmberKeyData()
        keyData.contents = key
        self.emberAddOrUpdateKeyTableEntry(address, True, keyData)
        self.TCRequestNetworkKeyUpdate()



    def TCHasLinkKey(self, address):
        keyStruct = ezsp.EmberKeyStruct()
        i = 0
        while i < self.EMBER_KEY_TABLE_SIZE:
            try:
                self.emberGetKeyTableEntry(i, keyStruct)
            except ezsp.EmberStatus as e:
                if e.value != ezsp.EMBER_TABLE_ENTRY_ERASED:
                    raise 
            else:
                if keyStruct.partnerEUI64 == address:
                    return True
            i += 1

        return False



    def TCDeleteKey(self, address):
        index = self.emberFindKeyTableEntry(address, True)
        if index == 255:
            return ezsp.EMBER_KEY_TABLE_INVALID_ADDRESS
        self.emberEraseKeyTableEntry(index)



    def TCDeleteAllKeys(self):
        index = 0
        while index < self.EMBER_KEY_TABLE_SIZE:
            self.emberEraseKeyTableEntry(index)
            index += 1




    def TCStartNetworkKeyUpdates(self):
        self.logger.info('TC: Starting automatic network key updates')
        self._networkKeyState = TC_NWK_KEY_WAIT
        self._networkKeyCount = TC_NETWORK_KEY_UPDATE_PERIOD_MINS
        self._requestKeyUpdate = False
        self.ezspSetTimer(0, 1, ezsp.EMBER_EVENT_MINUTE_TIME, True)



    def TCStopNetworkKeyUpdates(self):
        self.logger.info('TC: Stopping automatic network key updates')
        self.ezspSetTimer(0, 0, ezsp.EMBER_EVENT_INACTIVE, False)



    def TCRequestNetworkKeyUpdate(self):
        self.logger.info('TC: Network key update requested')
        self._requestKeyUpdate = True



    def _keyToString(self, key):
        s = '%02x%02x%02x%02x%02x%02x%02x%02x' % (key[0],
         key[1],
         key[2],
         key[3],
         key[4],
         key[5],
         key[6],
         key[7])
        s += '%02x%02x%02x%02x%02x%02x%02x%02x' % (key[8],
         key[9],
         key[10],
         key[11],
         key[12],
         key[13],
         key[14],
         key[15])
        return s



    def getKeyTableInformationString(self):
        keyTypeDict = {ezsp.EMBER_TRUST_CENTER_LINK_KEY: 'TC_LINK_KEY',
         ezsp.EMBER_TRUST_CENTER_MASTER_KEY: 'TC_MASTER_KEY',
         ezsp.EMBER_CURRENT_NETWORK_KEY: 'CURRENT_NWK_KEY',
         ezsp.EMBER_NEXT_NETWORK_KEY: 'NEXT_NWK_KEY',
         ezsp.EMBER_APPLICATION_LINK_KEY: 'APP_LINK_KEY',
         ezsp.EMBER_APPLICATION_MASTER_KEY: 'APP_MASTER_KEY'}
        keyStruct = ezsp.EmberKeyStruct()
        s = 'Keys:\n'
        for key in keyTypeDict:
            s += '%16s' % keyTypeDict[key]
            s += ' : '
            try:
                self.emberGetKey(key, keyStruct)
                s += byte_tuple.tupleToHexString(keyStruct.key.contents, 16)
            except ezsp.EmberStatus as e:
                s += str(e)
            s += '\n'

        s += '\nLink keys:\n'
        s += 'Indx Address            Key                                Type\n'
        i = 0
        while i < self.EMBER_KEY_TABLE_SIZE:
            s += '0x%02x ' % i
            try:
                self.emberGetKeyTableEntry(i, keyStruct)
                s += '%s ' % byte_tuple.eui64ToHexString(keyStruct.partnerEUI64)
                s += '%s ' % byte_tuple.tupleToHexString(keyStruct.key.contents, 16)
                s += '%s' % keyTypeDict[keyStruct.type]
                s += '\n'
            except ezsp.EmberStatus as e:
                s += '%s\n' % str(e)
            i += 1

        return s



    def _TCTimer0Tick(self):
        self.logger.debug('TC: Timer tick')
        if self._networkKeyState == TC_NWK_KEY_WAIT:
            if self._requestKeyUpdate == True:
                self._networkKeyState = TC_NWK_KEY_UPDATE
                self._requestKeyUpdate = False
            else:
                if self._networkKeyCount > 0:
                    self._networkKeyCount -= 1
                if self._networkKeyCount == 0:
                    self._networkKeyState = TC_NWK_KEY_UPDATE
        if self._networkKeyState == TC_NWK_KEY_UPDATE:
            self.logger.info('TC: Updating network key')
            if self.TCNetworkKeyUpdate():
                self._networkKeyState = TC_NWK_KEY_SWITCH
        elif self._networkKeyState == TC_NWK_KEY_SWITCH:
            self.logger.info('TC: Switching network key')
            if self.TCNetworkKeySwitch():
                self._networkKeyCount = TC_NETWORK_KEY_UPDATE_PERIOD_MINS
                self._networkKeyState = TC_NWK_KEY_WAIT



    def _TCStackStatusHandler(self, status):
        if status == ezsp.EMBER_NETWORK_UP or status == ezsp.EMBER_TRUST_CENTER_EUI_HAS_CHANGED:
            self.TCStartNetworkKeyUpdates()
        if status == ezsp.EMBER_NETWORK_DOWN:
            self.TCStopNetworkKeyUpdates()



    def callback_ezspTrustCenterJoinHandler(self, newNodeId, newNodeEui64, status, policyDecision, parentOfNewNodeId):
        policyDict = {ezsp.EMBER_USE_PRECONFIGURED_KEY: 'Allow (USE_PRECONFIGURED_KEY)',
         ezsp.EMBER_SEND_KEY_IN_THE_CLEAR: 'Allow (SEND_KEY_IN_THE_CLEAR)',
         ezsp.EMBER_DENY_JOIN: 'DENY_JOIN',
         ezsp.EMBER_NO_ACTION: 'NO_ACTION'}
        statusDict = {ezsp.EMBER_STANDARD_SECURITY_SECURED_REJOIN: 'STANDARD_SECURITY_SECURED_REJOIN',
         ezsp.EMBER_STANDARD_SECURITY_UNSECURED_JOIN: 'STANDARD_SECURITY_UNSECURED_JOIN',
         ezsp.EMBER_DEVICE_LEFT: 'DEVICE_LEFT',
         ezsp.EMBER_STANDARD_SECURITY_UNSECURED_REJOIN: 'STANDARD_SECURITY_UNSECURED_REJOIN',
         ezsp.EMBER_HIGH_SECURITY_SECURED_REJOIN: 'HIGH_SECURITY_SECURED_REJOIN',
         ezsp.EMBER_HIGH_SECURITY_UNSECURED_REJOIN: 'HIGH_SECURITY_UNSECURED_REJOIN'}
        try:
            self.logger.info('Trust Center: %s %s: %s' % (byte_tuple.eui64ToHexString(newNodeEui64), statusDict[status], policyDict[policyDecision]))
        except KeyError:
            self.logger.info('Trust Center: %s status = 0x%02x: decision = 0x%02x' % (byte_tuple.eui64ToHexString(newNodeEui64), status, policyDecision))
        if status == ezsp.EMBER_STANDARD_SECURITY_UNSECURED_JOIN and policyDecision == ezsp.EMBER_USE_PRECONFIGURED_KEY:
            self._weminucheLinkKeyRequiredCallback(newNodeEui64)




+++ okay decompyling ./trust_center.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2016.01.27 00:42:59 MSK
