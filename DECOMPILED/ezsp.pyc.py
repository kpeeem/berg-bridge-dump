# 2016.01.27 00:42:39 MSK
from sys import version_info
if version_info >= (2, 6, 0):

    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            (fp, pathname, description,) = imp.find_module('_ezsp', [dirname(__file__)])
        except ImportError:
            import _ezsp
            return _ezsp
        if fp is not None:
            try:
                _mod = imp.load_module('_ezsp', fp, pathname, description)
            finally:
                fp.close()
            return _mod


    _ezsp = swig_import_helper()
    del swig_import_helper
else:
    import _ezsp
del version_info
try:
    _swig_property = property
except NameError:
    pass

def _swig_setattr_nondynamic(self, class_type, name, value, static = 1):
    if name == 'thisown':
        return self.this.own(value)
    if name == 'this':
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return 
    method = class_type.__swig_setmethods__.get(name, None)
    if method:
        return method(self, value)
    if not static:
        self.__dict__[name] = value
    else:
        raise AttributeError('You cannot add attributes to %s' % self)



def _swig_setattr(self, class_type, name, value):
    return _swig_setattr_nondynamic(self, class_type, name, value, 0)



def _swig_getattr(self, class_type, name):
    if name == 'thisown':
        return self.this.own()
    method = class_type.__swig_getmethods__.get(name, None)
    if method:
        return method(self)
    raise AttributeError(name)



def _swig_repr(self):
    try:
        strthis = 'proxy of ' + self.this.__repr__()
    except:
        strthis = ''
    return '<%s.%s; %s >' % (self.__class__.__module__, self.__class__.__name__, strthis)


try:
    _object = object
    _newclass = 1
except AttributeError:

    class _object():
        pass
    _newclass = 0
TRUE = _ezsp.TRUE
FALSE = _ezsp.FALSE
EMBER_VERSION_TYPE_PRE_RELEASE = _ezsp.EMBER_VERSION_TYPE_PRE_RELEASE
EMBER_VERSION_TYPE_GA = _ezsp.EMBER_VERSION_TYPE_GA

class EmberVersion(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, EmberVersion, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, EmberVersion, name)
    __repr__ = _swig_repr
    __swig_setmethods__['build'] = _ezsp.EmberVersion_build_set
    __swig_getmethods__['build'] = _ezsp.EmberVersion_build_get
    if _newclass:
        build = _swig_property(_ezsp.EmberVersion_build_get, _ezsp.EmberVersion_build_set)
    __swig_setmethods__['major'] = _ezsp.EmberVersion_major_set
    __swig_getmethods__['major'] = _ezsp.EmberVersion_major_get
    if _newclass:
        major = _swig_property(_ezsp.EmberVersion_major_get, _ezsp.EmberVersion_major_set)
    __swig_setmethods__['minor'] = _ezsp.EmberVersion_minor_set
    __swig_getmethods__['minor'] = _ezsp.EmberVersion_minor_get
    if _newclass:
        minor = _swig_property(_ezsp.EmberVersion_minor_get, _ezsp.EmberVersion_minor_set)
    __swig_setmethods__['patch'] = _ezsp.EmberVersion_patch_set
    __swig_getmethods__['patch'] = _ezsp.EmberVersion_patch_get
    if _newclass:
        patch = _swig_property(_ezsp.EmberVersion_patch_get, _ezsp.EmberVersion_patch_set)
    __swig_setmethods__['special'] = _ezsp.EmberVersion_special_set
    __swig_getmethods__['special'] = _ezsp.EmberVersion_special_get
    if _newclass:
        special = _swig_property(_ezsp.EmberVersion_special_get, _ezsp.EmberVersion_special_set)
    __swig_setmethods__['type'] = _ezsp.EmberVersion_type_set
    __swig_getmethods__['type'] = _ezsp.EmberVersion_type_get
    if _newclass:
        type = _swig_property(_ezsp.EmberVersion_type_get, _ezsp.EmberVersion_type_set)

    def __init__(self):
        this = _ezsp.new_EmberVersion()
        try:
            self.this.append(this)
        except:
            self.this = this


    __swig_destroy__ = _ezsp.delete_EmberVersion
    __del__ = lambda self: None

EmberVersion_swigregister = _ezsp.EmberVersion_swigregister
EmberVersion_swigregister(EmberVersion)
EUI64_SIZE = _ezsp.EUI64_SIZE
EXTENDED_PAN_ID_SIZE = _ezsp.EXTENDED_PAN_ID_SIZE
EMBER_ENCRYPTION_KEY_SIZE = _ezsp.EMBER_ENCRYPTION_KEY_SIZE
EMBER_CERTIFICATE_SIZE = _ezsp.EMBER_CERTIFICATE_SIZE
EMBER_PUBLIC_KEY_SIZE = _ezsp.EMBER_PUBLIC_KEY_SIZE
EMBER_PRIVATE_KEY_SIZE = _ezsp.EMBER_PRIVATE_KEY_SIZE
EMBER_SMAC_SIZE = _ezsp.EMBER_SMAC_SIZE
EMBER_SIGNATURE_SIZE = _ezsp.EMBER_SIGNATURE_SIZE
EMBER_AES_HASH_BLOCK_SIZE = _ezsp.EMBER_AES_HASH_BLOCK_SIZE
EMBER_MAX_802_15_4_CHANNEL_NUMBER = _ezsp.EMBER_MAX_802_15_4_CHANNEL_NUMBER
EMBER_MIN_802_15_4_CHANNEL_NUMBER = _ezsp.EMBER_MIN_802_15_4_CHANNEL_NUMBER
EMBER_NUM_802_15_4_CHANNELS = _ezsp.EMBER_NUM_802_15_4_CHANNELS
EMBER_ALL_802_15_4_CHANNELS_MASK = _ezsp.EMBER_ALL_802_15_4_CHANNELS_MASK
EMBER_ZIGBEE_COORDINATOR_ADDRESS = _ezsp.EMBER_ZIGBEE_COORDINATOR_ADDRESS
EMBER_NULL_NODE_ID = _ezsp.EMBER_NULL_NODE_ID
EMBER_NULL_BINDING = _ezsp.EMBER_NULL_BINDING
EMBER_TABLE_ENTRY_UNUSED_NODE_ID = _ezsp.EMBER_TABLE_ENTRY_UNUSED_NODE_ID
EMBER_MULTICAST_NODE_ID = _ezsp.EMBER_MULTICAST_NODE_ID
EMBER_UNKNOWN_NODE_ID = _ezsp.EMBER_UNKNOWN_NODE_ID
EMBER_DISCOVERY_ACTIVE_NODE_ID = _ezsp.EMBER_DISCOVERY_ACTIVE_NODE_ID
EMBER_NULL_ADDRESS_TABLE_INDEX = _ezsp.EMBER_NULL_ADDRESS_TABLE_INDEX
EMBER_ZDO_ENDPOINT = _ezsp.EMBER_ZDO_ENDPOINT
EMBER_BROADCAST_ENDPOINT = _ezsp.EMBER_BROADCAST_ENDPOINT
EMBER_ZDO_PROFILE_ID = _ezsp.EMBER_ZDO_PROFILE_ID
EMBER_WILDCARD_PROFILE_ID = _ezsp.EMBER_WILDCARD_PROFILE_ID
EMBER_MAXIMUM_STANDARD_PROFILE_ID = _ezsp.EMBER_MAXIMUM_STANDARD_PROFILE_ID
EMBER_BROADCAST_TABLE_TIMEOUT_QS = _ezsp.EMBER_BROADCAST_TABLE_TIMEOUT_QS
EMBER_ZIGBEE_LEAVE_AND_REJOIN = _ezsp.EMBER_ZIGBEE_LEAVE_AND_REJOIN
EMBER_ZIGBEE_LEAVE_AND_REMOVE_CHILDREN = _ezsp.EMBER_ZIGBEE_LEAVE_AND_REMOVE_CHILDREN
EMBER_LEAVE_REASON_NONE = _ezsp.EMBER_LEAVE_REASON_NONE
EMBER_LEAVE_DUE_TO_NWK_LEAVE_MESSAGE = _ezsp.EMBER_LEAVE_DUE_TO_NWK_LEAVE_MESSAGE
EMBER_LEAVE_DUE_TO_APS_REMOVE_MESSAGE = _ezsp.EMBER_LEAVE_DUE_TO_APS_REMOVE_MESSAGE
EMBER_LEAVE_DUE_TO_ZDO_LEAVE_MESSAGE = _ezsp.EMBER_LEAVE_DUE_TO_ZDO_LEAVE_MESSAGE
EMBER_LEAVE_DUE_TO_ZLL_TOUCHLINK = _ezsp.EMBER_LEAVE_DUE_TO_ZLL_TOUCHLINK
EMBER_LEAVE_DUE_TO_APP_EVENT_1 = _ezsp.EMBER_LEAVE_DUE_TO_APP_EVENT_1
EMBER_BROADCAST_ADDRESS = _ezsp.EMBER_BROADCAST_ADDRESS
EMBER_RX_ON_WHEN_IDLE_BROADCAST_ADDRESS = _ezsp.EMBER_RX_ON_WHEN_IDLE_BROADCAST_ADDRESS
EMBER_SLEEPY_BROADCAST_ADDRESS = _ezsp.EMBER_SLEEPY_BROADCAST_ADDRESS
EMBER_UNKNOWN_DEVICE = _ezsp.EMBER_UNKNOWN_DEVICE
EMBER_COORDINATOR = _ezsp.EMBER_COORDINATOR
EMBER_ROUTER = _ezsp.EMBER_ROUTER
EMBER_END_DEVICE = _ezsp.EMBER_END_DEVICE
EMBER_SLEEPY_END_DEVICE = _ezsp.EMBER_SLEEPY_END_DEVICE
EMBER_MOBILE_END_DEVICE = _ezsp.EMBER_MOBILE_END_DEVICE

class EmberZigbeeNetwork(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, EmberZigbeeNetwork, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, EmberZigbeeNetwork, name)
    __repr__ = _swig_repr
    __swig_setmethods__['panId'] = _ezsp.EmberZigbeeNetwork_panId_set
    __swig_getmethods__['panId'] = _ezsp.EmberZigbeeNetwork_panId_get
    if _newclass:
        panId = _swig_property(_ezsp.EmberZigbeeNetwork_panId_get, _ezsp.EmberZigbeeNetwork_panId_set)
    __swig_setmethods__['channel'] = _ezsp.EmberZigbeeNetwork_channel_set
    __swig_getmethods__['channel'] = _ezsp.EmberZigbeeNetwork_channel_get
    if _newclass:
        channel = _swig_property(_ezsp.EmberZigbeeNetwork_channel_get, _ezsp.EmberZigbeeNetwork_channel_set)
    __swig_setmethods__['allowingJoin'] = _ezsp.EmberZigbeeNetwork_allowingJoin_set
    __swig_getmethods__['allowingJoin'] = _ezsp.EmberZigbeeNetwork_allowingJoin_get
    if _newclass:
        allowingJoin = _swig_property(_ezsp.EmberZigbeeNetwork_allowingJoin_get, _ezsp.EmberZigbeeNetwork_allowingJoin_set)
    __swig_setmethods__['extendedPanId'] = _ezsp.EmberZigbeeNetwork_extendedPanId_set
    __swig_getmethods__['extendedPanId'] = _ezsp.EmberZigbeeNetwork_extendedPanId_get
    if _newclass:
        extendedPanId = _swig_property(_ezsp.EmberZigbeeNetwork_extendedPanId_get, _ezsp.EmberZigbeeNetwork_extendedPanId_set)
    __swig_setmethods__['stackProfile'] = _ezsp.EmberZigbeeNetwork_stackProfile_set
    __swig_getmethods__['stackProfile'] = _ezsp.EmberZigbeeNetwork_stackProfile_get
    if _newclass:
        stackProfile = _swig_property(_ezsp.EmberZigbeeNetwork_stackProfile_get, _ezsp.EmberZigbeeNetwork_stackProfile_set)
    __swig_setmethods__['nwkUpdateId'] = _ezsp.EmberZigbeeNetwork_nwkUpdateId_set
    __swig_getmethods__['nwkUpdateId'] = _ezsp.EmberZigbeeNetwork_nwkUpdateId_get
    if _newclass:
        nwkUpdateId = _swig_property(_ezsp.EmberZigbeeNetwork_nwkUpdateId_get, _ezsp.EmberZigbeeNetwork_nwkUpdateId_set)

    def __init__(self):
        this = _ezsp.new_EmberZigbeeNetwork()
        try:
            self.this.append(this)
        except:
            self.this = this


    __swig_destroy__ = _ezsp.delete_EmberZigbeeNetwork
    __del__ = lambda self: None

EmberZigbeeNetwork_swigregister = _ezsp.EmberZigbeeNetwork_swigregister
EmberZigbeeNetwork_swigregister(EmberZigbeeNetwork)
EMBER_NETWORK_INIT_NO_OPTIONS = _ezsp.EMBER_NETWORK_INIT_NO_OPTIONS
EMBER_NETWORK_INIT_PARENT_INFO_IN_TOKEN = _ezsp.EMBER_NETWORK_INIT_PARENT_INFO_IN_TOKEN

class EmberNetworkInitStruct(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, EmberNetworkInitStruct, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, EmberNetworkInitStruct, name)
    __repr__ = _swig_repr
    __swig_setmethods__['bitmask'] = _ezsp.EmberNetworkInitStruct_bitmask_set
    __swig_getmethods__['bitmask'] = _ezsp.EmberNetworkInitStruct_bitmask_get
    if _newclass:
        bitmask = _swig_property(_ezsp.EmberNetworkInitStruct_bitmask_get, _ezsp.EmberNetworkInitStruct_bitmask_set)

    def __init__(self):
        this = _ezsp.new_EmberNetworkInitStruct()
        try:
            self.this.append(this)
        except:
            self.this = this


    __swig_destroy__ = _ezsp.delete_EmberNetworkInitStruct
    __del__ = lambda self: None

EmberNetworkInitStruct_swigregister = _ezsp.EmberNetworkInitStruct_swigregister
EmberNetworkInitStruct_swigregister(EmberNetworkInitStruct)
EMBER_APS_OPTION_NONE = _ezsp.EMBER_APS_OPTION_NONE
EMBER_APS_OPTION_DSA_SIGN = _ezsp.EMBER_APS_OPTION_DSA_SIGN
EMBER_APS_OPTION_ENCRYPTION = _ezsp.EMBER_APS_OPTION_ENCRYPTION
EMBER_APS_OPTION_RETRY = _ezsp.EMBER_APS_OPTION_RETRY
EMBER_APS_OPTION_ENABLE_ROUTE_DISCOVERY = _ezsp.EMBER_APS_OPTION_ENABLE_ROUTE_DISCOVERY
EMBER_APS_OPTION_FORCE_ROUTE_DISCOVERY = _ezsp.EMBER_APS_OPTION_FORCE_ROUTE_DISCOVERY
EMBER_APS_OPTION_SOURCE_EUI64 = _ezsp.EMBER_APS_OPTION_SOURCE_EUI64
EMBER_APS_OPTION_DESTINATION_EUI64 = _ezsp.EMBER_APS_OPTION_DESTINATION_EUI64
EMBER_APS_OPTION_ENABLE_ADDRESS_DISCOVERY = _ezsp.EMBER_APS_OPTION_ENABLE_ADDRESS_DISCOVERY
EMBER_APS_OPTION_POLL_RESPONSE = _ezsp.EMBER_APS_OPTION_POLL_RESPONSE
EMBER_APS_OPTION_ZDO_RESPONSE_REQUIRED = _ezsp.EMBER_APS_OPTION_ZDO_RESPONSE_REQUIRED
EMBER_APS_OPTION_FRAGMENT = _ezsp.EMBER_APS_OPTION_FRAGMENT
EMBER_INCOMING_UNICAST = _ezsp.EMBER_INCOMING_UNICAST
EMBER_INCOMING_UNICAST_REPLY = _ezsp.EMBER_INCOMING_UNICAST_REPLY
EMBER_INCOMING_MULTICAST = _ezsp.EMBER_INCOMING_MULTICAST
EMBER_INCOMING_MULTICAST_LOOPBACK = _ezsp.EMBER_INCOMING_MULTICAST_LOOPBACK
EMBER_INCOMING_BROADCAST = _ezsp.EMBER_INCOMING_BROADCAST
EMBER_INCOMING_BROADCAST_LOOPBACK = _ezsp.EMBER_INCOMING_BROADCAST_LOOPBACK
EMBER_OUTGOING_DIRECT = _ezsp.EMBER_OUTGOING_DIRECT
EMBER_OUTGOING_VIA_ADDRESS_TABLE = _ezsp.EMBER_OUTGOING_VIA_ADDRESS_TABLE
EMBER_OUTGOING_VIA_BINDING = _ezsp.EMBER_OUTGOING_VIA_BINDING
EMBER_OUTGOING_MULTICAST = _ezsp.EMBER_OUTGOING_MULTICAST
EMBER_OUTGOING_BROADCAST = _ezsp.EMBER_OUTGOING_BROADCAST
EMBER_NO_NETWORK = _ezsp.EMBER_NO_NETWORK
EMBER_JOINING_NETWORK = _ezsp.EMBER_JOINING_NETWORK
EMBER_JOINED_NETWORK = _ezsp.EMBER_JOINED_NETWORK
EMBER_JOINED_NETWORK_NO_PARENT = _ezsp.EMBER_JOINED_NETWORK_NO_PARENT
EMBER_LEAVING_NETWORK = _ezsp.EMBER_LEAVING_NETWORK
EMBER_ENERGY_SCAN = _ezsp.EMBER_ENERGY_SCAN
EMBER_ACTIVE_SCAN = _ezsp.EMBER_ACTIVE_SCAN
EMBER_UNUSED_BINDING = _ezsp.EMBER_UNUSED_BINDING
EMBER_UNICAST_BINDING = _ezsp.EMBER_UNICAST_BINDING
EMBER_MANY_TO_ONE_BINDING = _ezsp.EMBER_MANY_TO_ONE_BINDING
EMBER_MULTICAST_BINDING = _ezsp.EMBER_MULTICAST_BINDING
EMBER_LOW_RAM_CONCENTRATOR = _ezsp.EMBER_LOW_RAM_CONCENTRATOR
EMBER_HIGH_RAM_CONCENTRATOR = _ezsp.EMBER_HIGH_RAM_CONCENTRATOR
EMBER_USE_PRECONFIGURED_KEY = _ezsp.EMBER_USE_PRECONFIGURED_KEY
EMBER_SEND_KEY_IN_THE_CLEAR = _ezsp.EMBER_SEND_KEY_IN_THE_CLEAR
EMBER_DENY_JOIN = _ezsp.EMBER_DENY_JOIN
EMBER_NO_ACTION = _ezsp.EMBER_NO_ACTION
EMBER_STANDARD_SECURITY_SECURED_REJOIN = _ezsp.EMBER_STANDARD_SECURITY_SECURED_REJOIN
EMBER_STANDARD_SECURITY_UNSECURED_JOIN = _ezsp.EMBER_STANDARD_SECURITY_UNSECURED_JOIN
EMBER_DEVICE_LEFT = _ezsp.EMBER_DEVICE_LEFT
EMBER_STANDARD_SECURITY_UNSECURED_REJOIN = _ezsp.EMBER_STANDARD_SECURITY_UNSECURED_REJOIN
EMBER_HIGH_SECURITY_SECURED_REJOIN = _ezsp.EMBER_HIGH_SECURITY_SECURED_REJOIN
EMBER_HIGH_SECURITY_UNSECURED_JOIN = _ezsp.EMBER_HIGH_SECURITY_UNSECURED_JOIN
EMBER_HIGH_SECURITY_UNSECURED_REJOIN = _ezsp.EMBER_HIGH_SECURITY_UNSECURED_REJOIN
EMBER_REJOIN_REASON_NONE = _ezsp.EMBER_REJOIN_REASON_NONE
EMBER_REJOIN_DUE_TO_NWK_KEY_UPDATE = _ezsp.EMBER_REJOIN_DUE_TO_NWK_KEY_UPDATE
EMBER_REJOIN_DUE_TO_LEAVE_MESSAGE = _ezsp.EMBER_REJOIN_DUE_TO_LEAVE_MESSAGE
EMBER_REJOIN_DUE_TO_NO_PARENT = _ezsp.EMBER_REJOIN_DUE_TO_NO_PARENT
EMBER_REJOIN_DUE_TO_ZLL_TOUCHLINK = _ezsp.EMBER_REJOIN_DUE_TO_ZLL_TOUCHLINK
EMBER_REJOIN_DUE_TO_APP_EVENT_5 = _ezsp.EMBER_REJOIN_DUE_TO_APP_EVENT_5
EMBER_REJOIN_DUE_TO_APP_EVENT_4 = _ezsp.EMBER_REJOIN_DUE_TO_APP_EVENT_4
EMBER_REJOIN_DUE_TO_APP_EVENT_3 = _ezsp.EMBER_REJOIN_DUE_TO_APP_EVENT_3
EMBER_REJOIN_DUE_TO_APP_EVENT_2 = _ezsp.EMBER_REJOIN_DUE_TO_APP_EVENT_2
EMBER_REJOIN_DUE_TO_APP_EVENT_1 = _ezsp.EMBER_REJOIN_DUE_TO_APP_EVENT_1
EMBER_INPUT_CLUSTER_LIST = _ezsp.EMBER_INPUT_CLUSTER_LIST
EMBER_OUTPUT_CLUSTER_LIST = _ezsp.EMBER_OUTPUT_CLUSTER_LIST
EMBER_EVENT_INACTIVE = _ezsp.EMBER_EVENT_INACTIVE
EMBER_EVENT_MS_TIME = _ezsp.EMBER_EVENT_MS_TIME
EMBER_EVENT_QS_TIME = _ezsp.EMBER_EVENT_QS_TIME
EMBER_EVENT_MINUTE_TIME = _ezsp.EMBER_EVENT_MINUTE_TIME
EMBER_EVENT_ZERO_DELAY = _ezsp.EMBER_EVENT_ZERO_DELAY
EMBER_USE_MAC_ASSOCIATION = _ezsp.EMBER_USE_MAC_ASSOCIATION
EMBER_USE_NWK_REJOIN = _ezsp.EMBER_USE_NWK_REJOIN
EMBER_USE_NWK_REJOIN_HAVE_NWK_KEY = _ezsp.EMBER_USE_NWK_REJOIN_HAVE_NWK_KEY
EMBER_USE_NWK_COMMISSIONING = _ezsp.EMBER_USE_NWK_COMMISSIONING

class EmberNetworkParameters(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, EmberNetworkParameters, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, EmberNetworkParameters, name)
    __repr__ = _swig_repr
    __swig_setmethods__['extendedPanId'] = _ezsp.EmberNetworkParameters_extendedPanId_set
    __swig_getmethods__['extendedPanId'] = _ezsp.EmberNetworkParameters_extendedPanId_get
    if _newclass:
        extendedPanId = _swig_property(_ezsp.EmberNetworkParameters_extendedPanId_get, _ezsp.EmberNetworkParameters_extendedPanId_set)
    __swig_setmethods__['panId'] = _ezsp.EmberNetworkParameters_panId_set
    __swig_getmethods__['panId'] = _ezsp.EmberNetworkParameters_panId_get
    if _newclass:
        panId = _swig_property(_ezsp.EmberNetworkParameters_panId_get, _ezsp.EmberNetworkParameters_panId_set)
    __swig_setmethods__['radioTxPower'] = _ezsp.EmberNetworkParameters_radioTxPower_set
    __swig_getmethods__['radioTxPower'] = _ezsp.EmberNetworkParameters_radioTxPower_get
    if _newclass:
        radioTxPower = _swig_property(_ezsp.EmberNetworkParameters_radioTxPower_get, _ezsp.EmberNetworkParameters_radioTxPower_set)
    __swig_setmethods__['radioChannel'] = _ezsp.EmberNetworkParameters_radioChannel_set
    __swig_getmethods__['radioChannel'] = _ezsp.EmberNetworkParameters_radioChannel_get
    if _newclass:
        radioChannel = _swig_property(_ezsp.EmberNetworkParameters_radioChannel_get, _ezsp.EmberNetworkParameters_radioChannel_set)
    __swig_setmethods__['joinMethod'] = _ezsp.EmberNetworkParameters_joinMethod_set
    __swig_getmethods__['joinMethod'] = _ezsp.EmberNetworkParameters_joinMethod_get
    if _newclass:
        joinMethod = _swig_property(_ezsp.EmberNetworkParameters_joinMethod_get, _ezsp.EmberNetworkParameters_joinMethod_set)
    __swig_setmethods__['nwkManagerId'] = _ezsp.EmberNetworkParameters_nwkManagerId_set
    __swig_getmethods__['nwkManagerId'] = _ezsp.EmberNetworkParameters_nwkManagerId_get
    if _newclass:
        nwkManagerId = _swig_property(_ezsp.EmberNetworkParameters_nwkManagerId_get, _ezsp.EmberNetworkParameters_nwkManagerId_set)
    __swig_setmethods__['nwkUpdateId'] = _ezsp.EmberNetworkParameters_nwkUpdateId_set
    __swig_getmethods__['nwkUpdateId'] = _ezsp.EmberNetworkParameters_nwkUpdateId_get
    if _newclass:
        nwkUpdateId = _swig_property(_ezsp.EmberNetworkParameters_nwkUpdateId_get, _ezsp.EmberNetworkParameters_nwkUpdateId_set)
    __swig_setmethods__['channels'] = _ezsp.EmberNetworkParameters_channels_set
    __swig_getmethods__['channels'] = _ezsp.EmberNetworkParameters_channels_get
    if _newclass:
        channels = _swig_property(_ezsp.EmberNetworkParameters_channels_get, _ezsp.EmberNetworkParameters_channels_set)

    def __init__(self):
        this = _ezsp.new_EmberNetworkParameters()
        try:
            self.this.append(this)
        except:
            self.this = this


    __swig_destroy__ = _ezsp.delete_EmberNetworkParameters
    __del__ = lambda self: None

EmberNetworkParameters_swigregister = _ezsp.EmberNetworkParameters_swigregister
EmberNetworkParameters_swigregister(EmberNetworkParameters)

class EmberApsFrame(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, EmberApsFrame, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, EmberApsFrame, name)
    __repr__ = _swig_repr
    __swig_setmethods__['profileId'] = _ezsp.EmberApsFrame_profileId_set
    __swig_getmethods__['profileId'] = _ezsp.EmberApsFrame_profileId_get
    if _newclass:
        profileId = _swig_property(_ezsp.EmberApsFrame_profileId_get, _ezsp.EmberApsFrame_profileId_set)
    __swig_setmethods__['clusterId'] = _ezsp.EmberApsFrame_clusterId_set
    __swig_getmethods__['clusterId'] = _ezsp.EmberApsFrame_clusterId_get
    if _newclass:
        clusterId = _swig_property(_ezsp.EmberApsFrame_clusterId_get, _ezsp.EmberApsFrame_clusterId_set)
    __swig_setmethods__['sourceEndpoint'] = _ezsp.EmberApsFrame_sourceEndpoint_set
    __swig_getmethods__['sourceEndpoint'] = _ezsp.EmberApsFrame_sourceEndpoint_get
    if _newclass:
        sourceEndpoint = _swig_property(_ezsp.EmberApsFrame_sourceEndpoint_get, _ezsp.EmberApsFrame_sourceEndpoint_set)
    __swig_setmethods__['destinationEndpoint'] = _ezsp.EmberApsFrame_destinationEndpoint_set
    __swig_getmethods__['destinationEndpoint'] = _ezsp.EmberApsFrame_destinationEndpoint_get
    if _newclass:
        destinationEndpoint = _swig_property(_ezsp.EmberApsFrame_destinationEndpoint_get, _ezsp.EmberApsFrame_destinationEndpoint_set)
    __swig_setmethods__['options'] = _ezsp.EmberApsFrame_options_set
    __swig_getmethods__['options'] = _ezsp.EmberApsFrame_options_get
    if _newclass:
        options = _swig_property(_ezsp.EmberApsFrame_options_get, _ezsp.EmberApsFrame_options_set)
    __swig_setmethods__['groupId'] = _ezsp.EmberApsFrame_groupId_set
    __swig_getmethods__['groupId'] = _ezsp.EmberApsFrame_groupId_get
    if _newclass:
        groupId = _swig_property(_ezsp.EmberApsFrame_groupId_get, _ezsp.EmberApsFrame_groupId_set)
    __swig_setmethods__['sequence'] = _ezsp.EmberApsFrame_sequence_set
    __swig_getmethods__['sequence'] = _ezsp.EmberApsFrame_sequence_get
    if _newclass:
        sequence = _swig_property(_ezsp.EmberApsFrame_sequence_get, _ezsp.EmberApsFrame_sequence_set)

    def __init__(self):
        this = _ezsp.new_EmberApsFrame()
        try:
            self.this.append(this)
        except:
            self.this = this


    __swig_destroy__ = _ezsp.delete_EmberApsFrame
    __del__ = lambda self: None

EmberApsFrame_swigregister = _ezsp.EmberApsFrame_swigregister
EmberApsFrame_swigregister(EmberApsFrame)

class EmberBindingTableEntry(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, EmberBindingTableEntry, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, EmberBindingTableEntry, name)
    __repr__ = _swig_repr
    __swig_setmethods__['type'] = _ezsp.EmberBindingTableEntry_type_set
    __swig_getmethods__['type'] = _ezsp.EmberBindingTableEntry_type_get
    if _newclass:
        type = _swig_property(_ezsp.EmberBindingTableEntry_type_get, _ezsp.EmberBindingTableEntry_type_set)
    __swig_setmethods__['local'] = _ezsp.EmberBindingTableEntry_local_set
    __swig_getmethods__['local'] = _ezsp.EmberBindingTableEntry_local_get
    if _newclass:
        local = _swig_property(_ezsp.EmberBindingTableEntry_local_get, _ezsp.EmberBindingTableEntry_local_set)
    __swig_setmethods__['clusterId'] = _ezsp.EmberBindingTableEntry_clusterId_set
    __swig_getmethods__['clusterId'] = _ezsp.EmberBindingTableEntry_clusterId_get
    if _newclass:
        clusterId = _swig_property(_ezsp.EmberBindingTableEntry_clusterId_get, _ezsp.EmberBindingTableEntry_clusterId_set)
    __swig_setmethods__['remote'] = _ezsp.EmberBindingTableEntry_remote_set
    __swig_getmethods__['remote'] = _ezsp.EmberBindingTableEntry_remote_get
    if _newclass:
        remote = _swig_property(_ezsp.EmberBindingTableEntry_remote_get, _ezsp.EmberBindingTableEntry_remote_set)
    __swig_setmethods__['identifier'] = _ezsp.EmberBindingTableEntry_identifier_set
    __swig_getmethods__['identifier'] = _ezsp.EmberBindingTableEntry_identifier_get
    if _newclass:
        identifier = _swig_property(_ezsp.EmberBindingTableEntry_identifier_get, _ezsp.EmberBindingTableEntry_identifier_set)
    __swig_setmethods__['networkIndex'] = _ezsp.EmberBindingTableEntry_networkIndex_set
    __swig_getmethods__['networkIndex'] = _ezsp.EmberBindingTableEntry_networkIndex_get
    if _newclass:
        networkIndex = _swig_property(_ezsp.EmberBindingTableEntry_networkIndex_get, _ezsp.EmberBindingTableEntry_networkIndex_set)

    def __init__(self):
        this = _ezsp.new_EmberBindingTableEntry()
        try:
            self.this.append(this)
        except:
            self.this = this


    __swig_destroy__ = _ezsp.delete_EmberBindingTableEntry
    __del__ = lambda self: None

EmberBindingTableEntry_swigregister = _ezsp.EmberBindingTableEntry_swigregister
EmberBindingTableEntry_swigregister(EmberBindingTableEntry)

class EmberNeighborTableEntry(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, EmberNeighborTableEntry, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, EmberNeighborTableEntry, name)
    __repr__ = _swig_repr
    __swig_setmethods__['shortId'] = _ezsp.EmberNeighborTableEntry_shortId_set
    __swig_getmethods__['shortId'] = _ezsp.EmberNeighborTableEntry_shortId_get
    if _newclass:
        shortId = _swig_property(_ezsp.EmberNeighborTableEntry_shortId_get, _ezsp.EmberNeighborTableEntry_shortId_set)
    __swig_setmethods__['averageLqi'] = _ezsp.EmberNeighborTableEntry_averageLqi_set
    __swig_getmethods__['averageLqi'] = _ezsp.EmberNeighborTableEntry_averageLqi_get
    if _newclass:
        averageLqi = _swig_property(_ezsp.EmberNeighborTableEntry_averageLqi_get, _ezsp.EmberNeighborTableEntry_averageLqi_set)
    __swig_setmethods__['inCost'] = _ezsp.EmberNeighborTableEntry_inCost_set
    __swig_getmethods__['inCost'] = _ezsp.EmberNeighborTableEntry_inCost_get
    if _newclass:
        inCost = _swig_property(_ezsp.EmberNeighborTableEntry_inCost_get, _ezsp.EmberNeighborTableEntry_inCost_set)
    __swig_setmethods__['outCost'] = _ezsp.EmberNeighborTableEntry_outCost_set
    __swig_getmethods__['outCost'] = _ezsp.EmberNeighborTableEntry_outCost_get
    if _newclass:
        outCost = _swig_property(_ezsp.EmberNeighborTableEntry_outCost_get, _ezsp.EmberNeighborTableEntry_outCost_set)
    __swig_setmethods__['age'] = _ezsp.EmberNeighborTableEntry_age_set
    __swig_getmethods__['age'] = _ezsp.EmberNeighborTableEntry_age_get
    if _newclass:
        age = _swig_property(_ezsp.EmberNeighborTableEntry_age_get, _ezsp.EmberNeighborTableEntry_age_set)
    __swig_setmethods__['longId'] = _ezsp.EmberNeighborTableEntry_longId_set
    __swig_getmethods__['longId'] = _ezsp.EmberNeighborTableEntry_longId_get
    if _newclass:
        longId = _swig_property(_ezsp.EmberNeighborTableEntry_longId_get, _ezsp.EmberNeighborTableEntry_longId_set)

    def __init__(self):
        this = _ezsp.new_EmberNeighborTableEntry()
        try:
            self.this.append(this)
        except:
            self.this = this


    __swig_destroy__ = _ezsp.delete_EmberNeighborTableEntry
    __del__ = lambda self: None

EmberNeighborTableEntry_swigregister = _ezsp.EmberNeighborTableEntry_swigregister
EmberNeighborTableEntry_swigregister(EmberNeighborTableEntry)

class EmberRouteTableEntry(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, EmberRouteTableEntry, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, EmberRouteTableEntry, name)
    __repr__ = _swig_repr
    __swig_setmethods__['destination'] = _ezsp.EmberRouteTableEntry_destination_set
    __swig_getmethods__['destination'] = _ezsp.EmberRouteTableEntry_destination_get
    if _newclass:
        destination = _swig_property(_ezsp.EmberRouteTableEntry_destination_get, _ezsp.EmberRouteTableEntry_destination_set)
    __swig_setmethods__['nextHop'] = _ezsp.EmberRouteTableEntry_nextHop_set
    __swig_getmethods__['nextHop'] = _ezsp.EmberRouteTableEntry_nextHop_get
    if _newclass:
        nextHop = _swig_property(_ezsp.EmberRouteTableEntry_nextHop_get, _ezsp.EmberRouteTableEntry_nextHop_set)
    __swig_setmethods__['status'] = _ezsp.EmberRouteTableEntry_status_set
    __swig_getmethods__['status'] = _ezsp.EmberRouteTableEntry_status_get
    if _newclass:
        status = _swig_property(_ezsp.EmberRouteTableEntry_status_get, _ezsp.EmberRouteTableEntry_status_set)
    __swig_setmethods__['age'] = _ezsp.EmberRouteTableEntry_age_set
    __swig_getmethods__['age'] = _ezsp.EmberRouteTableEntry_age_get
    if _newclass:
        age = _swig_property(_ezsp.EmberRouteTableEntry_age_get, _ezsp.EmberRouteTableEntry_age_set)
    __swig_setmethods__['concentratorType'] = _ezsp.EmberRouteTableEntry_concentratorType_set
    __swig_getmethods__['concentratorType'] = _ezsp.EmberRouteTableEntry_concentratorType_get
    if _newclass:
        concentratorType = _swig_property(_ezsp.EmberRouteTableEntry_concentratorType_get, _ezsp.EmberRouteTableEntry_concentratorType_set)
    __swig_setmethods__['routeRecordState'] = _ezsp.EmberRouteTableEntry_routeRecordState_set
    __swig_getmethods__['routeRecordState'] = _ezsp.EmberRouteTableEntry_routeRecordState_get
    if _newclass:
        routeRecordState = _swig_property(_ezsp.EmberRouteTableEntry_routeRecordState_get, _ezsp.EmberRouteTableEntry_routeRecordState_set)

    def __init__(self):
        this = _ezsp.new_EmberRouteTableEntry()
        try:
            self.this.append(this)
        except:
            self.this = this


    __swig_destroy__ = _ezsp.delete_EmberRouteTableEntry
    __del__ = lambda self: None

EmberRouteTableEntry_swigregister = _ezsp.EmberRouteTableEntry_swigregister
EmberRouteTableEntry_swigregister(EmberRouteTableEntry)

class EmberMulticastTableEntry(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, EmberMulticastTableEntry, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, EmberMulticastTableEntry, name)
    __repr__ = _swig_repr
    __swig_setmethods__['multicastId'] = _ezsp.EmberMulticastTableEntry_multicastId_set
    __swig_getmethods__['multicastId'] = _ezsp.EmberMulticastTableEntry_multicastId_get
    if _newclass:
        multicastId = _swig_property(_ezsp.EmberMulticastTableEntry_multicastId_get, _ezsp.EmberMulticastTableEntry_multicastId_set)
    __swig_setmethods__['endpoint'] = _ezsp.EmberMulticastTableEntry_endpoint_set
    __swig_getmethods__['endpoint'] = _ezsp.EmberMulticastTableEntry_endpoint_get
    if _newclass:
        endpoint = _swig_property(_ezsp.EmberMulticastTableEntry_endpoint_get, _ezsp.EmberMulticastTableEntry_endpoint_set)
    __swig_setmethods__['networkIndex'] = _ezsp.EmberMulticastTableEntry_networkIndex_set
    __swig_getmethods__['networkIndex'] = _ezsp.EmberMulticastTableEntry_networkIndex_get
    if _newclass:
        networkIndex = _swig_property(_ezsp.EmberMulticastTableEntry_networkIndex_get, _ezsp.EmberMulticastTableEntry_networkIndex_set)

    def __init__(self):
        this = _ezsp.new_EmberMulticastTableEntry()
        try:
            self.this.append(this)
        except:
            self.this = this


    __swig_destroy__ = _ezsp.delete_EmberMulticastTableEntry
    __del__ = lambda self: None

EmberMulticastTableEntry_swigregister = _ezsp.EmberMulticastTableEntry_swigregister
EmberMulticastTableEntry_swigregister(EmberMulticastTableEntry)
EMBER_COUNTER_MAC_RX_BROADCAST = _ezsp.EMBER_COUNTER_MAC_RX_BROADCAST
EMBER_COUNTER_MAC_TX_BROADCAST = _ezsp.EMBER_COUNTER_MAC_TX_BROADCAST
EMBER_COUNTER_MAC_RX_UNICAST = _ezsp.EMBER_COUNTER_MAC_RX_UNICAST
EMBER_COUNTER_MAC_TX_UNICAST_SUCCESS = _ezsp.EMBER_COUNTER_MAC_TX_UNICAST_SUCCESS
EMBER_COUNTER_MAC_TX_UNICAST_RETRY = _ezsp.EMBER_COUNTER_MAC_TX_UNICAST_RETRY
EMBER_COUNTER_MAC_TX_UNICAST_FAILED = _ezsp.EMBER_COUNTER_MAC_TX_UNICAST_FAILED
EMBER_COUNTER_APS_DATA_RX_BROADCAST = _ezsp.EMBER_COUNTER_APS_DATA_RX_BROADCAST
EMBER_COUNTER_APS_DATA_TX_BROADCAST = _ezsp.EMBER_COUNTER_APS_DATA_TX_BROADCAST
EMBER_COUNTER_APS_DATA_RX_UNICAST = _ezsp.EMBER_COUNTER_APS_DATA_RX_UNICAST
EMBER_COUNTER_APS_DATA_TX_UNICAST_SUCCESS = _ezsp.EMBER_COUNTER_APS_DATA_TX_UNICAST_SUCCESS
EMBER_COUNTER_APS_DATA_TX_UNICAST_RETRY = _ezsp.EMBER_COUNTER_APS_DATA_TX_UNICAST_RETRY
EMBER_COUNTER_APS_DATA_TX_UNICAST_FAILED = _ezsp.EMBER_COUNTER_APS_DATA_TX_UNICAST_FAILED
EMBER_COUNTER_ROUTE_DISCOVERY_INITIATED = _ezsp.EMBER_COUNTER_ROUTE_DISCOVERY_INITIATED
EMBER_COUNTER_NEIGHBOR_ADDED = _ezsp.EMBER_COUNTER_NEIGHBOR_ADDED
EMBER_COUNTER_NEIGHBOR_REMOVED = _ezsp.EMBER_COUNTER_NEIGHBOR_REMOVED
EMBER_COUNTER_NEIGHBOR_STALE = _ezsp.EMBER_COUNTER_NEIGHBOR_STALE
EMBER_COUNTER_JOIN_INDICATION = _ezsp.EMBER_COUNTER_JOIN_INDICATION
EMBER_COUNTER_CHILD_REMOVED = _ezsp.EMBER_COUNTER_CHILD_REMOVED
EMBER_COUNTER_ASH_OVERFLOW_ERROR = _ezsp.EMBER_COUNTER_ASH_OVERFLOW_ERROR
EMBER_COUNTER_ASH_FRAMING_ERROR = _ezsp.EMBER_COUNTER_ASH_FRAMING_ERROR
EMBER_COUNTER_ASH_OVERRUN_ERROR = _ezsp.EMBER_COUNTER_ASH_OVERRUN_ERROR
EMBER_COUNTER_NWK_FRAME_COUNTER_FAILURE = _ezsp.EMBER_COUNTER_NWK_FRAME_COUNTER_FAILURE
EMBER_COUNTER_APS_FRAME_COUNTER_FAILURE = _ezsp.EMBER_COUNTER_APS_FRAME_COUNTER_FAILURE
EMBER_COUNTER_ASH_XOFF = _ezsp.EMBER_COUNTER_ASH_XOFF
EMBER_COUNTER_APS_LINK_KEY_NOT_AUTHORIZED = _ezsp.EMBER_COUNTER_APS_LINK_KEY_NOT_AUTHORIZED
EMBER_COUNTER_NWK_DECRYPTION_FAILURE = _ezsp.EMBER_COUNTER_NWK_DECRYPTION_FAILURE
EMBER_COUNTER_APS_DECRYPTION_FAILURE = _ezsp.EMBER_COUNTER_APS_DECRYPTION_FAILURE
EMBER_COUNTER_ALLOCATE_PACKET_BUFFER_FAILURE = _ezsp.EMBER_COUNTER_ALLOCATE_PACKET_BUFFER_FAILURE
EMBER_COUNTER_RELAYED_UNICAST = _ezsp.EMBER_COUNTER_RELAYED_UNICAST
EMBER_COUNTER_PHY_TO_MAC_QUEUE_LIMIT_REACHED = _ezsp.EMBER_COUNTER_PHY_TO_MAC_QUEUE_LIMIT_REACHED
EMBER_COUNTER_PACKET_VALIDATE_LIBRARY_DROPPED_COUNT = _ezsp.EMBER_COUNTER_PACKET_VALIDATE_LIBRARY_DROPPED_COUNT
EMBER_COUNTER_TYPE_COUNT = _ezsp.EMBER_COUNTER_TYPE_COUNT
EMBER_TX_POWER_MODE_DEFAULT = _ezsp.EMBER_TX_POWER_MODE_DEFAULT
EMBER_TX_POWER_MODE_BOOST = _ezsp.EMBER_TX_POWER_MODE_BOOST
EMBER_TX_POWER_MODE_ALTERNATE = _ezsp.EMBER_TX_POWER_MODE_ALTERNATE
EMBER_TX_POWER_MODE_BOOST_AND_ALTERNATE = _ezsp.EMBER_TX_POWER_MODE_BOOST_AND_ALTERNATE
EMBER_TX_POWER_MODE_USE_TOKEN = _ezsp.EMBER_TX_POWER_MODE_USE_TOKEN
EMBER_PRIVATE_PROFILE_ID = _ezsp.EMBER_PRIVATE_PROFILE_ID
EMBER_BROADCAST_ALARM_CLUSTER = _ezsp.EMBER_BROADCAST_ALARM_CLUSTER
EMBER_UNICAST_ALARM_CLUSTER = _ezsp.EMBER_UNICAST_ALARM_CLUSTER
EMBER_CACHED_UNICAST_ALARM_CLUSTER = _ezsp.EMBER_CACHED_UNICAST_ALARM_CLUSTER
EMBER_REPORT_COUNTERS_REQUEST = _ezsp.EMBER_REPORT_COUNTERS_REQUEST
EMBER_REPORT_COUNTERS_RESPONSE = _ezsp.EMBER_REPORT_COUNTERS_RESPONSE
EMBER_REPORT_AND_CLEAR_COUNTERS_REQUEST = _ezsp.EMBER_REPORT_AND_CLEAR_COUNTERS_REQUEST
EMBER_REPORT_AND_CLEAR_COUNTERS_RESPONSE = _ezsp.EMBER_REPORT_AND_CLEAR_COUNTERS_RESPONSE
EMBER_OTA_CERTIFICATE_UPGRADE_CLUSTER = _ezsp.EMBER_OTA_CERTIFICATE_UPGRADE_CLUSTER

class EmberKeyData(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, EmberKeyData, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, EmberKeyData, name)
    __repr__ = _swig_repr
    __swig_setmethods__['contents'] = _ezsp.EmberKeyData_contents_set
    __swig_getmethods__['contents'] = _ezsp.EmberKeyData_contents_get
    if _newclass:
        contents = _swig_property(_ezsp.EmberKeyData_contents_get, _ezsp.EmberKeyData_contents_set)

    def __init__(self):
        this = _ezsp.new_EmberKeyData()
        try:
            self.this.append(this)
        except:
            self.this = this


    __swig_destroy__ = _ezsp.delete_EmberKeyData
    __del__ = lambda self: None

EmberKeyData_swigregister = _ezsp.EmberKeyData_swigregister
EmberKeyData_swigregister(EmberKeyData)

class EmberCertificateData(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, EmberCertificateData, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, EmberCertificateData, name)
    __repr__ = _swig_repr
    __swig_setmethods__['contents'] = _ezsp.EmberCertificateData_contents_set
    __swig_getmethods__['contents'] = _ezsp.EmberCertificateData_contents_get
    if _newclass:
        contents = _swig_property(_ezsp.EmberCertificateData_contents_get, _ezsp.EmberCertificateData_contents_set)

    def __init__(self):
        this = _ezsp.new_EmberCertificateData()
        try:
            self.this.append(this)
        except:
            self.this = this


    __swig_destroy__ = _ezsp.delete_EmberCertificateData
    __del__ = lambda self: None

EmberCertificateData_swigregister = _ezsp.EmberCertificateData_swigregister
EmberCertificateData_swigregister(EmberCertificateData)

class EmberPublicKeyData(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, EmberPublicKeyData, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, EmberPublicKeyData, name)
    __repr__ = _swig_repr
    __swig_setmethods__['contents'] = _ezsp.EmberPublicKeyData_contents_set
    __swig_getmethods__['contents'] = _ezsp.EmberPublicKeyData_contents_get
    if _newclass:
        contents = _swig_property(_ezsp.EmberPublicKeyData_contents_get, _ezsp.EmberPublicKeyData_contents_set)

    def __init__(self):
        this = _ezsp.new_EmberPublicKeyData()
        try:
            self.this.append(this)
        except:
            self.this = this


    __swig_destroy__ = _ezsp.delete_EmberPublicKeyData
    __del__ = lambda self: None

EmberPublicKeyData_swigregister = _ezsp.EmberPublicKeyData_swigregister
EmberPublicKeyData_swigregister(EmberPublicKeyData)

class EmberPrivateKeyData(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, EmberPrivateKeyData, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, EmberPrivateKeyData, name)
    __repr__ = _swig_repr
    __swig_setmethods__['contents'] = _ezsp.EmberPrivateKeyData_contents_set
    __swig_getmethods__['contents'] = _ezsp.EmberPrivateKeyData_contents_get
    if _newclass:
        contents = _swig_property(_ezsp.EmberPrivateKeyData_contents_get, _ezsp.EmberPrivateKeyData_contents_set)

    def __init__(self):
        this = _ezsp.new_EmberPrivateKeyData()
        try:
            self.this.append(this)
        except:
            self.this = this


    __swig_destroy__ = _ezsp.delete_EmberPrivateKeyData
    __del__ = lambda self: None

EmberPrivateKeyData_swigregister = _ezsp.EmberPrivateKeyData_swigregister
EmberPrivateKeyData_swigregister(EmberPrivateKeyData)

class EmberSmacData(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, EmberSmacData, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, EmberSmacData, name)
    __repr__ = _swig_repr
    __swig_setmethods__['contents'] = _ezsp.EmberSmacData_contents_set
    __swig_getmethods__['contents'] = _ezsp.EmberSmacData_contents_get
    if _newclass:
        contents = _swig_property(_ezsp.EmberSmacData_contents_get, _ezsp.EmberSmacData_contents_set)

    def __init__(self):
        this = _ezsp.new_EmberSmacData()
        try:
            self.this.append(this)
        except:
            self.this = this


    __swig_destroy__ = _ezsp.delete_EmberSmacData
    __del__ = lambda self: None

EmberSmacData_swigregister = _ezsp.EmberSmacData_swigregister
EmberSmacData_swigregister(EmberSmacData)

class EmberSignatureData(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, EmberSignatureData, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, EmberSignatureData, name)
    __repr__ = _swig_repr
    __swig_setmethods__['contents'] = _ezsp.EmberSignatureData_contents_set
    __swig_getmethods__['contents'] = _ezsp.EmberSignatureData_contents_get
    if _newclass:
        contents = _swig_property(_ezsp.EmberSignatureData_contents_get, _ezsp.EmberSignatureData_contents_set)

    def __init__(self):
        this = _ezsp.new_EmberSignatureData()
        try:
            self.this.append(this)
        except:
            self.this = this


    __swig_destroy__ = _ezsp.delete_EmberSignatureData
    __del__ = lambda self: None

EmberSignatureData_swigregister = _ezsp.EmberSignatureData_swigregister
EmberSignatureData_swigregister(EmberSignatureData)

class EmberMessageDigest(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, EmberMessageDigest, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, EmberMessageDigest, name)
    __repr__ = _swig_repr
    __swig_setmethods__['contents'] = _ezsp.EmberMessageDigest_contents_set
    __swig_getmethods__['contents'] = _ezsp.EmberMessageDigest_contents_get
    if _newclass:
        contents = _swig_property(_ezsp.EmberMessageDigest_contents_get, _ezsp.EmberMessageDigest_contents_set)

    def __init__(self):
        this = _ezsp.new_EmberMessageDigest()
        try:
            self.this.append(this)
        except:
            self.this = this


    __swig_destroy__ = _ezsp.delete_EmberMessageDigest
    __del__ = lambda self: None

EmberMessageDigest_swigregister = _ezsp.EmberMessageDigest_swigregister
EmberMessageDigest_swigregister(EmberMessageDigest)

class EmberAesMmoHashContext(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, EmberAesMmoHashContext, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, EmberAesMmoHashContext, name)
    __repr__ = _swig_repr
    __swig_setmethods__['result'] = _ezsp.EmberAesMmoHashContext_result_set
    __swig_getmethods__['result'] = _ezsp.EmberAesMmoHashContext_result_get
    if _newclass:
        result = _swig_property(_ezsp.EmberAesMmoHashContext_result_get, _ezsp.EmberAesMmoHashContext_result_set)
    __swig_setmethods__['length'] = _ezsp.EmberAesMmoHashContext_length_set
    __swig_getmethods__['length'] = _ezsp.EmberAesMmoHashContext_length_get
    if _newclass:
        length = _swig_property(_ezsp.EmberAesMmoHashContext_length_get, _ezsp.EmberAesMmoHashContext_length_set)

    def __init__(self):
        this = _ezsp.new_EmberAesMmoHashContext()
        try:
            self.this.append(this)
        except:
            self.this = this


    __swig_destroy__ = _ezsp.delete_EmberAesMmoHashContext
    __del__ = lambda self: None

EmberAesMmoHashContext_swigregister = _ezsp.EmberAesMmoHashContext_swigregister
EmberAesMmoHashContext_swigregister(EmberAesMmoHashContext)
EMBER_STANDARD_SECURITY_MODE = _ezsp.EMBER_STANDARD_SECURITY_MODE
EMBER_TRUST_CENTER_NODE_ID = _ezsp.EMBER_TRUST_CENTER_NODE_ID
EMBER_DISTRIBUTED_TRUST_CENTER_MODE = _ezsp.EMBER_DISTRIBUTED_TRUST_CENTER_MODE
EMBER_TRUST_CENTER_GLOBAL_LINK_KEY = _ezsp.EMBER_TRUST_CENTER_GLOBAL_LINK_KEY
EMBER_PRECONFIGURED_NETWORK_KEY_MODE = _ezsp.EMBER_PRECONFIGURED_NETWORK_KEY_MODE
EMBER_HAVE_TRUST_CENTER_UNKNOWN_KEY_TOKEN = _ezsp.EMBER_HAVE_TRUST_CENTER_UNKNOWN_KEY_TOKEN
EMBER_HAVE_TRUST_CENTER_LINK_KEY_TOKEN = _ezsp.EMBER_HAVE_TRUST_CENTER_LINK_KEY_TOKEN
EMBER_HAVE_TRUST_CENTER_MASTER_KEY_TOKEN = _ezsp.EMBER_HAVE_TRUST_CENTER_MASTER_KEY_TOKEN
EMBER_HAVE_TRUST_CENTER_EUI64 = _ezsp.EMBER_HAVE_TRUST_CENTER_EUI64
EMBER_TRUST_CENTER_USES_HASHED_LINK_KEY = _ezsp.EMBER_TRUST_CENTER_USES_HASHED_LINK_KEY
EMBER_HAVE_PRECONFIGURED_KEY = _ezsp.EMBER_HAVE_PRECONFIGURED_KEY
EMBER_HAVE_NETWORK_KEY = _ezsp.EMBER_HAVE_NETWORK_KEY
EMBER_GET_LINK_KEY_WHEN_JOINING = _ezsp.EMBER_GET_LINK_KEY_WHEN_JOINING
EMBER_REQUIRE_ENCRYPTED_KEY = _ezsp.EMBER_REQUIRE_ENCRYPTED_KEY
EMBER_NO_FRAME_COUNTER_RESET = _ezsp.EMBER_NO_FRAME_COUNTER_RESET
EMBER_GET_PRECONFIGURED_KEY_FROM_INSTALL_CODE = _ezsp.EMBER_GET_PRECONFIGURED_KEY_FROM_INSTALL_CODE
EM_SAVED_IN_TOKEN = _ezsp.EM_SAVED_IN_TOKEN
EM_SECURITY_INITIALIZED = _ezsp.EM_SECURITY_INITIALIZED
NO_TRUST_CENTER_KEY_TOKEN = _ezsp.NO_TRUST_CENTER_KEY_TOKEN
TRUST_CENTER_KEY_TOKEN_MASK = _ezsp.TRUST_CENTER_KEY_TOKEN_MASK
SECURITY_BIT_TOKEN_MASK = _ezsp.SECURITY_BIT_TOKEN_MASK
SECURITY_LOWER_BIT_MASK = _ezsp.SECURITY_LOWER_BIT_MASK
SECURITY_UPPER_BIT_MASK = _ezsp.SECURITY_UPPER_BIT_MASK

class EmberInitialSecurityState(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, EmberInitialSecurityState, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, EmberInitialSecurityState, name)
    __repr__ = _swig_repr
    __swig_setmethods__['bitmask'] = _ezsp.EmberInitialSecurityState_bitmask_set
    __swig_getmethods__['bitmask'] = _ezsp.EmberInitialSecurityState_bitmask_get
    if _newclass:
        bitmask = _swig_property(_ezsp.EmberInitialSecurityState_bitmask_get, _ezsp.EmberInitialSecurityState_bitmask_set)
    __swig_setmethods__['preconfiguredKey'] = _ezsp.EmberInitialSecurityState_preconfiguredKey_set
    __swig_getmethods__['preconfiguredKey'] = _ezsp.EmberInitialSecurityState_preconfiguredKey_get
    if _newclass:
        preconfiguredKey = _swig_property(_ezsp.EmberInitialSecurityState_preconfiguredKey_get, _ezsp.EmberInitialSecurityState_preconfiguredKey_set)
    __swig_setmethods__['networkKey'] = _ezsp.EmberInitialSecurityState_networkKey_set
    __swig_getmethods__['networkKey'] = _ezsp.EmberInitialSecurityState_networkKey_get
    if _newclass:
        networkKey = _swig_property(_ezsp.EmberInitialSecurityState_networkKey_get, _ezsp.EmberInitialSecurityState_networkKey_set)
    __swig_setmethods__['networkKeySequenceNumber'] = _ezsp.EmberInitialSecurityState_networkKeySequenceNumber_set
    __swig_getmethods__['networkKeySequenceNumber'] = _ezsp.EmberInitialSecurityState_networkKeySequenceNumber_get
    if _newclass:
        networkKeySequenceNumber = _swig_property(_ezsp.EmberInitialSecurityState_networkKeySequenceNumber_get, _ezsp.EmberInitialSecurityState_networkKeySequenceNumber_set)
    __swig_setmethods__['preconfiguredTrustCenterEui64'] = _ezsp.EmberInitialSecurityState_preconfiguredTrustCenterEui64_set
    __swig_getmethods__['preconfiguredTrustCenterEui64'] = _ezsp.EmberInitialSecurityState_preconfiguredTrustCenterEui64_get
    if _newclass:
        preconfiguredTrustCenterEui64 = _swig_property(_ezsp.EmberInitialSecurityState_preconfiguredTrustCenterEui64_get, _ezsp.EmberInitialSecurityState_preconfiguredTrustCenterEui64_set)

    def __init__(self):
        this = _ezsp.new_EmberInitialSecurityState()
        try:
            self.this.append(this)
        except:
            self.this = this


    __swig_destroy__ = _ezsp.delete_EmberInitialSecurityState
    __del__ = lambda self: None

EmberInitialSecurityState_swigregister = _ezsp.EmberInitialSecurityState_swigregister
EmberInitialSecurityState_swigregister(EmberInitialSecurityState)
EMBER_HAVE_TRUST_CENTER_LINK_KEY = _ezsp.EMBER_HAVE_TRUST_CENTER_LINK_KEY
EMBER_TRUST_CENTER_USES_HASHED_LINK_KEY_ = _ezsp.EMBER_TRUST_CENTER_USES_HASHED_LINK_KEY_
INITIAL_AND_CURRENT_BITMASK = _ezsp.INITIAL_AND_CURRENT_BITMASK

class EmberCurrentSecurityState(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, EmberCurrentSecurityState, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, EmberCurrentSecurityState, name)
    __repr__ = _swig_repr
    __swig_setmethods__['bitmask'] = _ezsp.EmberCurrentSecurityState_bitmask_set
    __swig_getmethods__['bitmask'] = _ezsp.EmberCurrentSecurityState_bitmask_get
    if _newclass:
        bitmask = _swig_property(_ezsp.EmberCurrentSecurityState_bitmask_get, _ezsp.EmberCurrentSecurityState_bitmask_set)
    __swig_setmethods__['trustCenterLongAddress'] = _ezsp.EmberCurrentSecurityState_trustCenterLongAddress_set
    __swig_getmethods__['trustCenterLongAddress'] = _ezsp.EmberCurrentSecurityState_trustCenterLongAddress_get
    if _newclass:
        trustCenterLongAddress = _swig_property(_ezsp.EmberCurrentSecurityState_trustCenterLongAddress_get, _ezsp.EmberCurrentSecurityState_trustCenterLongAddress_set)

    def __init__(self):
        this = _ezsp.new_EmberCurrentSecurityState()
        try:
            self.this.append(this)
        except:
            self.this = this


    __swig_destroy__ = _ezsp.delete_EmberCurrentSecurityState
    __del__ = lambda self: None

EmberCurrentSecurityState_swigregister = _ezsp.EmberCurrentSecurityState_swigregister
EmberCurrentSecurityState_swigregister(EmberCurrentSecurityState)
EMBER_KEY_HAS_SEQUENCE_NUMBER = _ezsp.EMBER_KEY_HAS_SEQUENCE_NUMBER
EMBER_KEY_HAS_OUTGOING_FRAME_COUNTER = _ezsp.EMBER_KEY_HAS_OUTGOING_FRAME_COUNTER
EMBER_KEY_HAS_INCOMING_FRAME_COUNTER = _ezsp.EMBER_KEY_HAS_INCOMING_FRAME_COUNTER
EMBER_KEY_HAS_PARTNER_EUI64 = _ezsp.EMBER_KEY_HAS_PARTNER_EUI64
EMBER_KEY_IS_AUTHORIZED = _ezsp.EMBER_KEY_IS_AUTHORIZED
EMBER_KEY_PARTNER_IS_SLEEPY = _ezsp.EMBER_KEY_PARTNER_IS_SLEEPY
EMBER_TRUST_CENTER_LINK_KEY = _ezsp.EMBER_TRUST_CENTER_LINK_KEY
EMBER_TRUST_CENTER_MASTER_KEY = _ezsp.EMBER_TRUST_CENTER_MASTER_KEY
EMBER_CURRENT_NETWORK_KEY = _ezsp.EMBER_CURRENT_NETWORK_KEY
EMBER_NEXT_NETWORK_KEY = _ezsp.EMBER_NEXT_NETWORK_KEY
EMBER_APPLICATION_LINK_KEY = _ezsp.EMBER_APPLICATION_LINK_KEY
EMBER_APPLICATION_MASTER_KEY = _ezsp.EMBER_APPLICATION_MASTER_KEY

class EmberKeyStruct(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, EmberKeyStruct, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, EmberKeyStruct, name)
    __repr__ = _swig_repr
    __swig_setmethods__['bitmask'] = _ezsp.EmberKeyStruct_bitmask_set
    __swig_getmethods__['bitmask'] = _ezsp.EmberKeyStruct_bitmask_get
    if _newclass:
        bitmask = _swig_property(_ezsp.EmberKeyStruct_bitmask_get, _ezsp.EmberKeyStruct_bitmask_set)
    __swig_setmethods__['type'] = _ezsp.EmberKeyStruct_type_set
    __swig_getmethods__['type'] = _ezsp.EmberKeyStruct_type_get
    if _newclass:
        type = _swig_property(_ezsp.EmberKeyStruct_type_get, _ezsp.EmberKeyStruct_type_set)
    __swig_setmethods__['key'] = _ezsp.EmberKeyStruct_key_set
    __swig_getmethods__['key'] = _ezsp.EmberKeyStruct_key_get
    if _newclass:
        key = _swig_property(_ezsp.EmberKeyStruct_key_get, _ezsp.EmberKeyStruct_key_set)
    __swig_setmethods__['outgoingFrameCounter'] = _ezsp.EmberKeyStruct_outgoingFrameCounter_set
    __swig_getmethods__['outgoingFrameCounter'] = _ezsp.EmberKeyStruct_outgoingFrameCounter_get
    if _newclass:
        outgoingFrameCounter = _swig_property(_ezsp.EmberKeyStruct_outgoingFrameCounter_get, _ezsp.EmberKeyStruct_outgoingFrameCounter_set)
    __swig_setmethods__['incomingFrameCounter'] = _ezsp.EmberKeyStruct_incomingFrameCounter_set
    __swig_getmethods__['incomingFrameCounter'] = _ezsp.EmberKeyStruct_incomingFrameCounter_get
    if _newclass:
        incomingFrameCounter = _swig_property(_ezsp.EmberKeyStruct_incomingFrameCounter_get, _ezsp.EmberKeyStruct_incomingFrameCounter_set)
    __swig_setmethods__['sequenceNumber'] = _ezsp.EmberKeyStruct_sequenceNumber_set
    __swig_getmethods__['sequenceNumber'] = _ezsp.EmberKeyStruct_sequenceNumber_get
    if _newclass:
        sequenceNumber = _swig_property(_ezsp.EmberKeyStruct_sequenceNumber_get, _ezsp.EmberKeyStruct_sequenceNumber_set)
    __swig_setmethods__['partnerEUI64'] = _ezsp.EmberKeyStruct_partnerEUI64_set
    __swig_getmethods__['partnerEUI64'] = _ezsp.EmberKeyStruct_partnerEUI64_get
    if _newclass:
        partnerEUI64 = _swig_property(_ezsp.EmberKeyStruct_partnerEUI64_get, _ezsp.EmberKeyStruct_partnerEUI64_set)

    def __init__(self):
        this = _ezsp.new_EmberKeyStruct()
        try:
            self.this.append(this)
        except:
            self.this = this


    __swig_destroy__ = _ezsp.delete_EmberKeyStruct
    __del__ = lambda self: None

EmberKeyStruct_swigregister = _ezsp.EmberKeyStruct_swigregister
EmberKeyStruct_swigregister(EmberKeyStruct)
EMBER_APP_LINK_KEY_ESTABLISHED = _ezsp.EMBER_APP_LINK_KEY_ESTABLISHED
EMBER_APP_MASTER_KEY_ESTABLISHED = _ezsp.EMBER_APP_MASTER_KEY_ESTABLISHED
EMBER_TRUST_CENTER_LINK_KEY_ESTABLISHED = _ezsp.EMBER_TRUST_CENTER_LINK_KEY_ESTABLISHED
EMBER_KEY_ESTABLISHMENT_TIMEOUT = _ezsp.EMBER_KEY_ESTABLISHMENT_TIMEOUT
EMBER_KEY_TABLE_FULL = _ezsp.EMBER_KEY_TABLE_FULL
EMBER_TC_RESPONDED_TO_KEY_REQUEST = _ezsp.EMBER_TC_RESPONDED_TO_KEY_REQUEST
EMBER_TC_APP_KEY_SENT_TO_REQUESTER = _ezsp.EMBER_TC_APP_KEY_SENT_TO_REQUESTER
EMBER_TC_RESPONSE_TO_KEY_REQUEST_FAILED = _ezsp.EMBER_TC_RESPONSE_TO_KEY_REQUEST_FAILED
EMBER_TC_REQUEST_KEY_TYPE_NOT_SUPPORTED = _ezsp.EMBER_TC_REQUEST_KEY_TYPE_NOT_SUPPORTED
EMBER_TC_NO_LINK_KEY_FOR_REQUESTER = _ezsp.EMBER_TC_NO_LINK_KEY_FOR_REQUESTER
EMBER_TC_REQUESTER_EUI64_UNKNOWN = _ezsp.EMBER_TC_REQUESTER_EUI64_UNKNOWN
EMBER_TC_RECEIVED_FIRST_APP_KEY_REQUEST = _ezsp.EMBER_TC_RECEIVED_FIRST_APP_KEY_REQUEST
EMBER_TC_TIMEOUT_WAITING_FOR_SECOND_APP_KEY_REQUEST = _ezsp.EMBER_TC_TIMEOUT_WAITING_FOR_SECOND_APP_KEY_REQUEST
EMBER_TC_NON_MATCHING_APP_KEY_REQUEST_RECEIVED = _ezsp.EMBER_TC_NON_MATCHING_APP_KEY_REQUEST_RECEIVED
EMBER_TC_FAILED_TO_SEND_APP_KEYS = _ezsp.EMBER_TC_FAILED_TO_SEND_APP_KEYS
EMBER_TC_FAILED_TO_STORE_APP_KEY_REQUEST = _ezsp.EMBER_TC_FAILED_TO_STORE_APP_KEY_REQUEST
EMBER_TC_REJECTED_APP_KEY_REQUEST = _ezsp.EMBER_TC_REJECTED_APP_KEY_REQUEST
EMBER_DENY_KEY_REQUESTS = _ezsp.EMBER_DENY_KEY_REQUESTS
EMBER_ALLOW_KEY_REQUESTS = _ezsp.EMBER_ALLOW_KEY_REQUESTS
EMBER_KEY_PERMISSIONS_NONE = _ezsp.EMBER_KEY_PERMISSIONS_NONE
EMBER_KEY_PERMISSIONS_READING_ALLOWED = _ezsp.EMBER_KEY_PERMISSIONS_READING_ALLOWED
EMBER_KEY_PERMISSIONS_HASHING_ALLOWED = _ezsp.EMBER_KEY_PERMISSIONS_HASHING_ALLOWED

class EmberMfgSecurityStruct(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, EmberMfgSecurityStruct, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, EmberMfgSecurityStruct, name)
    __repr__ = _swig_repr
    __swig_setmethods__['keySettings'] = _ezsp.EmberMfgSecurityStruct_keySettings_set
    __swig_getmethods__['keySettings'] = _ezsp.EmberMfgSecurityStruct_keySettings_get
    if _newclass:
        keySettings = _swig_property(_ezsp.EmberMfgSecurityStruct_keySettings_get, _ezsp.EmberMfgSecurityStruct_keySettings_set)

    def __init__(self):
        this = _ezsp.new_EmberMfgSecurityStruct()
        try:
            self.this.append(this)
        except:
            self.this = this


    __swig_destroy__ = _ezsp.delete_EmberMfgSecurityStruct
    __del__ = lambda self: None

EmberMfgSecurityStruct_swigregister = _ezsp.EmberMfgSecurityStruct_swigregister
EmberMfgSecurityStruct_swigregister(EmberMfgSecurityStruct)
EMBER_MFG_SECURITY_CONFIG_MAGIC_NUMBER = _ezsp.EMBER_MFG_SECURITY_CONFIG_MAGIC_NUMBER
EMBER_MAC_PASSTHROUGH_NONE = _ezsp.EMBER_MAC_PASSTHROUGH_NONE
EMBER_MAC_PASSTHROUGH_SE_INTERPAN = _ezsp.EMBER_MAC_PASSTHROUGH_SE_INTERPAN
EMBER_MAC_PASSTHROUGH_EMBERNET = _ezsp.EMBER_MAC_PASSTHROUGH_EMBERNET
EMBER_MAC_PASSTHROUGH_EMBERNET_SOURCE = _ezsp.EMBER_MAC_PASSTHROUGH_EMBERNET_SOURCE
EMBER_MAC_PASSTHROUGH_APPLICATION = _ezsp.EMBER_MAC_PASSTHROUGH_APPLICATION
EMBER_MAC_PASSTHROUGH_CUSTOM = _ezsp.EMBER_MAC_PASSTHROUGH_CUSTOM
EM_MAC_PASSTHROUGH_INTERNAL = _ezsp.EM_MAC_PASSTHROUGH_INTERNAL
EMBER_MAC_FILTER_MATCH_ENABLED_MASK = _ezsp.EMBER_MAC_FILTER_MATCH_ENABLED_MASK
EMBER_MAC_FILTER_MATCH_ON_PAN_DEST_MASK = _ezsp.EMBER_MAC_FILTER_MATCH_ON_PAN_DEST_MASK
EMBER_MAC_FILTER_MATCH_ON_PAN_SOURCE_MASK = _ezsp.EMBER_MAC_FILTER_MATCH_ON_PAN_SOURCE_MASK
EMBER_MAC_FILTER_MATCH_ON_DEST_MASK = _ezsp.EMBER_MAC_FILTER_MATCH_ON_DEST_MASK
EMBER_MAC_FILTER_MATCH_ON_SOURCE_MASK = _ezsp.EMBER_MAC_FILTER_MATCH_ON_SOURCE_MASK
EMBER_MAC_FILTER_MATCH_ENABLED = _ezsp.EMBER_MAC_FILTER_MATCH_ENABLED
EMBER_MAC_FILTER_MATCH_DISABLED = _ezsp.EMBER_MAC_FILTER_MATCH_DISABLED
EMBER_MAC_FILTER_MATCH_ON_PAN_DEST_NONE = _ezsp.EMBER_MAC_FILTER_MATCH_ON_PAN_DEST_NONE
EMBER_MAC_FILTER_MATCH_ON_PAN_DEST_LOCAL = _ezsp.EMBER_MAC_FILTER_MATCH_ON_PAN_DEST_LOCAL
EMBER_MAC_FILTER_MATCH_ON_PAN_DEST_BROADCAST = _ezsp.EMBER_MAC_FILTER_MATCH_ON_PAN_DEST_BROADCAST
EMBER_MAC_FILTER_MATCH_ON_PAN_SOURCE_NONE = _ezsp.EMBER_MAC_FILTER_MATCH_ON_PAN_SOURCE_NONE
EMBER_MAC_FILTER_MATCH_ON_PAN_SOURCE_NON_LOCAL = _ezsp.EMBER_MAC_FILTER_MATCH_ON_PAN_SOURCE_NON_LOCAL
EMBER_MAC_FILTER_MATCH_ON_PAN_SOURCE_LOCAL = _ezsp.EMBER_MAC_FILTER_MATCH_ON_PAN_SOURCE_LOCAL
EMBER_MAC_FILTER_MATCH_ON_DEST_BROADCAST_SHORT = _ezsp.EMBER_MAC_FILTER_MATCH_ON_DEST_BROADCAST_SHORT
EMBER_MAC_FILTER_MATCH_ON_DEST_UNICAST_SHORT = _ezsp.EMBER_MAC_FILTER_MATCH_ON_DEST_UNICAST_SHORT
EMBER_MAC_FILTER_MATCH_ON_DEST_UNICAST_LONG = _ezsp.EMBER_MAC_FILTER_MATCH_ON_DEST_UNICAST_LONG
EMBER_MAC_FILTER_MATCH_ON_SOURCE_LONG = _ezsp.EMBER_MAC_FILTER_MATCH_ON_SOURCE_LONG
EMBER_MAC_FILTER_MATCH_ON_SOURCE_SHORT = _ezsp.EMBER_MAC_FILTER_MATCH_ON_SOURCE_SHORT
EMBER_MAC_FILTER_MATCH_END = _ezsp.EMBER_MAC_FILTER_MATCH_END

class EmberMacFilterMatchStruct(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, EmberMacFilterMatchStruct, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, EmberMacFilterMatchStruct, name)
    __repr__ = _swig_repr
    __swig_setmethods__['filterIndexMatch'] = _ezsp.EmberMacFilterMatchStruct_filterIndexMatch_set
    __swig_getmethods__['filterIndexMatch'] = _ezsp.EmberMacFilterMatchStruct_filterIndexMatch_get
    if _newclass:
        filterIndexMatch = _swig_property(_ezsp.EmberMacFilterMatchStruct_filterIndexMatch_get, _ezsp.EmberMacFilterMatchStruct_filterIndexMatch_set)
    __swig_setmethods__['legacyPassthroughType'] = _ezsp.EmberMacFilterMatchStruct_legacyPassthroughType_set
    __swig_getmethods__['legacyPassthroughType'] = _ezsp.EmberMacFilterMatchStruct_legacyPassthroughType_get
    if _newclass:
        legacyPassthroughType = _swig_property(_ezsp.EmberMacFilterMatchStruct_legacyPassthroughType_get, _ezsp.EmberMacFilterMatchStruct_legacyPassthroughType_set)
    __swig_setmethods__['message'] = _ezsp.EmberMacFilterMatchStruct_message_set
    __swig_getmethods__['message'] = _ezsp.EmberMacFilterMatchStruct_message_get
    if _newclass:
        message = _swig_property(_ezsp.EmberMacFilterMatchStruct_message_get, _ezsp.EmberMacFilterMatchStruct_message_set)

    def __init__(self):
        this = _ezsp.new_EmberMacFilterMatchStruct()
        try:
            self.this.append(this)
        except:
            self.this = this


    __swig_destroy__ = _ezsp.delete_EmberMacFilterMatchStruct
    __del__ = lambda self: None

EmberMacFilterMatchStruct_swigregister = _ezsp.EmberMacFilterMatchStruct_swigregister
EmberMacFilterMatchStruct_swigregister(EmberMacFilterMatchStruct)
EMBER_ZDP_SUCCESS = _ezsp.EMBER_ZDP_SUCCESS
EMBER_ZDP_INVALID_REQUEST_TYPE = _ezsp.EMBER_ZDP_INVALID_REQUEST_TYPE
EMBER_ZDP_DEVICE_NOT_FOUND = _ezsp.EMBER_ZDP_DEVICE_NOT_FOUND
EMBER_ZDP_INVALID_ENDPOINT = _ezsp.EMBER_ZDP_INVALID_ENDPOINT
EMBER_ZDP_NOT_ACTIVE = _ezsp.EMBER_ZDP_NOT_ACTIVE
EMBER_ZDP_NOT_SUPPORTED = _ezsp.EMBER_ZDP_NOT_SUPPORTED
EMBER_ZDP_TIMEOUT = _ezsp.EMBER_ZDP_TIMEOUT
EMBER_ZDP_NO_MATCH = _ezsp.EMBER_ZDP_NO_MATCH
EMBER_ZDP_NO_ENTRY = _ezsp.EMBER_ZDP_NO_ENTRY
EMBER_ZDP_NO_DESCRIPTOR = _ezsp.EMBER_ZDP_NO_DESCRIPTOR
EMBER_ZDP_INSUFFICIENT_SPACE = _ezsp.EMBER_ZDP_INSUFFICIENT_SPACE
EMBER_ZDP_NOT_PERMITTED = _ezsp.EMBER_ZDP_NOT_PERMITTED
EMBER_ZDP_TABLE_FULL = _ezsp.EMBER_ZDP_TABLE_FULL
EMBER_ZDP_NOT_AUTHORIZED = _ezsp.EMBER_ZDP_NOT_AUTHORIZED
EMBER_NWK_ALREADY_PRESENT = _ezsp.EMBER_NWK_ALREADY_PRESENT
EMBER_NWK_TABLE_FULL = _ezsp.EMBER_NWK_TABLE_FULL
EMBER_NWK_UNKNOWN_DEVICE = _ezsp.EMBER_NWK_UNKNOWN_DEVICE
NETWORK_ADDRESS_REQUEST = _ezsp.NETWORK_ADDRESS_REQUEST
NETWORK_ADDRESS_RESPONSE = _ezsp.NETWORK_ADDRESS_RESPONSE
IEEE_ADDRESS_REQUEST = _ezsp.IEEE_ADDRESS_REQUEST
IEEE_ADDRESS_RESPONSE = _ezsp.IEEE_ADDRESS_RESPONSE
NODE_DESCRIPTOR_REQUEST = _ezsp.NODE_DESCRIPTOR_REQUEST
NODE_DESCRIPTOR_RESPONSE = _ezsp.NODE_DESCRIPTOR_RESPONSE
POWER_DESCRIPTOR_REQUEST = _ezsp.POWER_DESCRIPTOR_REQUEST
POWER_DESCRIPTOR_RESPONSE = _ezsp.POWER_DESCRIPTOR_RESPONSE
SIMPLE_DESCRIPTOR_REQUEST = _ezsp.SIMPLE_DESCRIPTOR_REQUEST
SIMPLE_DESCRIPTOR_RESPONSE = _ezsp.SIMPLE_DESCRIPTOR_RESPONSE
ACTIVE_ENDPOINTS_REQUEST = _ezsp.ACTIVE_ENDPOINTS_REQUEST
ACTIVE_ENDPOINTS_RESPONSE = _ezsp.ACTIVE_ENDPOINTS_RESPONSE
MATCH_DESCRIPTORS_REQUEST = _ezsp.MATCH_DESCRIPTORS_REQUEST
MATCH_DESCRIPTORS_RESPONSE = _ezsp.MATCH_DESCRIPTORS_RESPONSE
DISCOVERY_CACHE_REQUEST = _ezsp.DISCOVERY_CACHE_REQUEST
DISCOVERY_CACHE_RESPONSE = _ezsp.DISCOVERY_CACHE_RESPONSE
END_DEVICE_ANNOUNCE = _ezsp.END_DEVICE_ANNOUNCE
END_DEVICE_ANNOUNCE_RESPONSE = _ezsp.END_DEVICE_ANNOUNCE_RESPONSE
SYSTEM_SERVER_DISCOVERY_REQUEST = _ezsp.SYSTEM_SERVER_DISCOVERY_REQUEST
SYSTEM_SERVER_DISCOVERY_RESPONSE = _ezsp.SYSTEM_SERVER_DISCOVERY_RESPONSE
EMBER_ZDP_PRIMARY_TRUST_CENTER = _ezsp.EMBER_ZDP_PRIMARY_TRUST_CENTER
EMBER_ZDP_SECONDARY_TRUST_CENTER = _ezsp.EMBER_ZDP_SECONDARY_TRUST_CENTER
EMBER_ZDP_PRIMARY_BINDING_TABLE_CACHE = _ezsp.EMBER_ZDP_PRIMARY_BINDING_TABLE_CACHE
EMBER_ZDP_SECONDARY_BINDING_TABLE_CACHE = _ezsp.EMBER_ZDP_SECONDARY_BINDING_TABLE_CACHE
EMBER_ZDP_PRIMARY_DISCOVERY_CACHE = _ezsp.EMBER_ZDP_PRIMARY_DISCOVERY_CACHE
EMBER_ZDP_SECONDARY_DISCOVERY_CACHE = _ezsp.EMBER_ZDP_SECONDARY_DISCOVERY_CACHE
EMBER_ZDP_NETWORK_MANAGER = _ezsp.EMBER_ZDP_NETWORK_MANAGER
FIND_NODE_CACHE_REQUEST = _ezsp.FIND_NODE_CACHE_REQUEST
FIND_NODE_CACHE_RESPONSE = _ezsp.FIND_NODE_CACHE_RESPONSE
END_DEVICE_BIND_REQUEST = _ezsp.END_DEVICE_BIND_REQUEST
END_DEVICE_BIND_RESPONSE = _ezsp.END_DEVICE_BIND_RESPONSE
UNICAST_BINDING = _ezsp.UNICAST_BINDING
UNICAST_MANY_TO_ONE_BINDING = _ezsp.UNICAST_MANY_TO_ONE_BINDING
MULTICAST_BINDING = _ezsp.MULTICAST_BINDING
BIND_REQUEST = _ezsp.BIND_REQUEST
BIND_RESPONSE = _ezsp.BIND_RESPONSE
UNBIND_REQUEST = _ezsp.UNBIND_REQUEST
UNBIND_RESPONSE = _ezsp.UNBIND_RESPONSE
LQI_TABLE_REQUEST = _ezsp.LQI_TABLE_REQUEST
LQI_TABLE_RESPONSE = _ezsp.LQI_TABLE_RESPONSE
ROUTING_TABLE_REQUEST = _ezsp.ROUTING_TABLE_REQUEST
ROUTING_TABLE_RESPONSE = _ezsp.ROUTING_TABLE_RESPONSE
BINDING_TABLE_REQUEST = _ezsp.BINDING_TABLE_REQUEST
BINDING_TABLE_RESPONSE = _ezsp.BINDING_TABLE_RESPONSE
LEAVE_REQUEST = _ezsp.LEAVE_REQUEST
LEAVE_RESPONSE = _ezsp.LEAVE_RESPONSE
LEAVE_REQUEST_REMOVE_CHILDREN_FLAG = _ezsp.LEAVE_REQUEST_REMOVE_CHILDREN_FLAG
LEAVE_REQUEST_REJOIN_FLAG = _ezsp.LEAVE_REQUEST_REJOIN_FLAG
PERMIT_JOINING_REQUEST = _ezsp.PERMIT_JOINING_REQUEST
PERMIT_JOINING_RESPONSE = _ezsp.PERMIT_JOINING_RESPONSE
NWK_UPDATE_REQUEST = _ezsp.NWK_UPDATE_REQUEST
NWK_UPDATE_RESPONSE = _ezsp.NWK_UPDATE_RESPONSE
COMPLEX_DESCRIPTOR_REQUEST = _ezsp.COMPLEX_DESCRIPTOR_REQUEST
COMPLEX_DESCRIPTOR_RESPONSE = _ezsp.COMPLEX_DESCRIPTOR_RESPONSE
USER_DESCRIPTOR_REQUEST = _ezsp.USER_DESCRIPTOR_REQUEST
USER_DESCRIPTOR_RESPONSE = _ezsp.USER_DESCRIPTOR_RESPONSE
DISCOVERY_REGISTER_REQUEST = _ezsp.DISCOVERY_REGISTER_REQUEST
DISCOVERY_REGISTER_RESPONSE = _ezsp.DISCOVERY_REGISTER_RESPONSE
USER_DESCRIPTOR_SET = _ezsp.USER_DESCRIPTOR_SET
USER_DESCRIPTOR_CONFIRM = _ezsp.USER_DESCRIPTOR_CONFIRM
NETWORK_DISCOVERY_REQUEST = _ezsp.NETWORK_DISCOVERY_REQUEST
NETWORK_DISCOVERY_RESPONSE = _ezsp.NETWORK_DISCOVERY_RESPONSE
DIRECT_JOIN_REQUEST = _ezsp.DIRECT_JOIN_REQUEST
DIRECT_JOIN_RESPONSE = _ezsp.DIRECT_JOIN_RESPONSE
CLUSTER_ID_RESPONSE_MINIMUM = _ezsp.CLUSTER_ID_RESPONSE_MINIMUM
EMBER_APP_RECEIVES_SUPPORTED_ZDO_REQUESTS = _ezsp.EMBER_APP_RECEIVES_SUPPORTED_ZDO_REQUESTS
EMBER_APP_HANDLES_UNSUPPORTED_ZDO_REQUESTS = _ezsp.EMBER_APP_HANDLES_UNSUPPORTED_ZDO_REQUESTS
EMBER_APP_HANDLES_ZDO_ENDPOINT_REQUESTS = _ezsp.EMBER_APP_HANDLES_ZDO_ENDPOINT_REQUESTS
EMBER_APP_HANDLES_ZDO_BINDING_REQUESTS = _ezsp.EMBER_APP_HANDLES_ZDO_BINDING_REQUESTS
EZSP_CONFIG_PACKET_BUFFER_COUNT = _ezsp.EZSP_CONFIG_PACKET_BUFFER_COUNT
EZSP_CONFIG_NEIGHBOR_TABLE_SIZE = _ezsp.EZSP_CONFIG_NEIGHBOR_TABLE_SIZE
EZSP_CONFIG_APS_UNICAST_MESSAGE_COUNT = _ezsp.EZSP_CONFIG_APS_UNICAST_MESSAGE_COUNT
EZSP_CONFIG_BINDING_TABLE_SIZE = _ezsp.EZSP_CONFIG_BINDING_TABLE_SIZE
EZSP_CONFIG_ADDRESS_TABLE_SIZE = _ezsp.EZSP_CONFIG_ADDRESS_TABLE_SIZE
EZSP_CONFIG_MULTICAST_TABLE_SIZE = _ezsp.EZSP_CONFIG_MULTICAST_TABLE_SIZE
EZSP_CONFIG_ROUTE_TABLE_SIZE = _ezsp.EZSP_CONFIG_ROUTE_TABLE_SIZE
EZSP_CONFIG_DISCOVERY_TABLE_SIZE = _ezsp.EZSP_CONFIG_DISCOVERY_TABLE_SIZE
EZSP_CONFIG_BROADCAST_ALARM_DATA_SIZE = _ezsp.EZSP_CONFIG_BROADCAST_ALARM_DATA_SIZE
EZSP_CONFIG_UNICAST_ALARM_DATA_SIZE = _ezsp.EZSP_CONFIG_UNICAST_ALARM_DATA_SIZE
EZSP_CONFIG_STACK_PROFILE = _ezsp.EZSP_CONFIG_STACK_PROFILE
EZSP_CONFIG_SECURITY_LEVEL = _ezsp.EZSP_CONFIG_SECURITY_LEVEL
EZSP_CONFIG_MAX_HOPS = _ezsp.EZSP_CONFIG_MAX_HOPS
EZSP_CONFIG_MAX_END_DEVICE_CHILDREN = _ezsp.EZSP_CONFIG_MAX_END_DEVICE_CHILDREN
EZSP_CONFIG_INDIRECT_TRANSMISSION_TIMEOUT = _ezsp.EZSP_CONFIG_INDIRECT_TRANSMISSION_TIMEOUT
EZSP_CONFIG_END_DEVICE_POLL_TIMEOUT = _ezsp.EZSP_CONFIG_END_DEVICE_POLL_TIMEOUT
EZSP_CONFIG_MOBILE_NODE_POLL_TIMEOUT = _ezsp.EZSP_CONFIG_MOBILE_NODE_POLL_TIMEOUT
EZSP_CONFIG_RESERVED_MOBILE_CHILD_ENTRIES = _ezsp.EZSP_CONFIG_RESERVED_MOBILE_CHILD_ENTRIES
EZSP_CONFIG_TX_POWER_MODE = _ezsp.EZSP_CONFIG_TX_POWER_MODE
EZSP_CONFIG_DISABLE_RELAY = _ezsp.EZSP_CONFIG_DISABLE_RELAY
EZSP_CONFIG_TRUST_CENTER_ADDRESS_CACHE_SIZE = _ezsp.EZSP_CONFIG_TRUST_CENTER_ADDRESS_CACHE_SIZE
EZSP_CONFIG_SOURCE_ROUTE_TABLE_SIZE = _ezsp.EZSP_CONFIG_SOURCE_ROUTE_TABLE_SIZE
EZSP_CONFIG_END_DEVICE_POLL_TIMEOUT_SHIFT = _ezsp.EZSP_CONFIG_END_DEVICE_POLL_TIMEOUT_SHIFT
EZSP_CONFIG_FRAGMENT_WINDOW_SIZE = _ezsp.EZSP_CONFIG_FRAGMENT_WINDOW_SIZE
EZSP_CONFIG_FRAGMENT_DELAY_MS = _ezsp.EZSP_CONFIG_FRAGMENT_DELAY_MS
EZSP_CONFIG_KEY_TABLE_SIZE = _ezsp.EZSP_CONFIG_KEY_TABLE_SIZE
EZSP_CONFIG_APS_ACK_TIMEOUT = _ezsp.EZSP_CONFIG_APS_ACK_TIMEOUT
EZSP_CONFIG_ACTIVE_SCAN_DURATION = _ezsp.EZSP_CONFIG_ACTIVE_SCAN_DURATION
EZSP_CONFIG_END_DEVICE_BIND_TIMEOUT = _ezsp.EZSP_CONFIG_END_DEVICE_BIND_TIMEOUT
EZSP_CONFIG_PAN_ID_CONFLICT_REPORT_THRESHOLD = _ezsp.EZSP_CONFIG_PAN_ID_CONFLICT_REPORT_THRESHOLD
EZSP_CONFIG_REQUEST_KEY_TIMEOUT = _ezsp.EZSP_CONFIG_REQUEST_KEY_TIMEOUT
EZSP_CONFIG_CERTIFICATE_TABLE_SIZE = _ezsp.EZSP_CONFIG_CERTIFICATE_TABLE_SIZE
EZSP_CONFIG_APPLICATION_ZDO_FLAGS = _ezsp.EZSP_CONFIG_APPLICATION_ZDO_FLAGS
EZSP_CONFIG_BROADCAST_TABLE_SIZE = _ezsp.EZSP_CONFIG_BROADCAST_TABLE_SIZE
EZSP_CONFIG_MAC_FILTER_TABLE_SIZE = _ezsp.EZSP_CONFIG_MAC_FILTER_TABLE_SIZE
EZSP_CONFIG_SUPPORTED_NETWORKS = _ezsp.EZSP_CONFIG_SUPPORTED_NETWORKS
EZSP_CONFIG_SEND_MULTICASTS_TO_SLEEPY_ADDRESS = _ezsp.EZSP_CONFIG_SEND_MULTICASTS_TO_SLEEPY_ADDRESS
EZSP_CONFIG_ID_MAX = _ezsp.EZSP_CONFIG_ID_MAX
EZSP_VALUE_TOKEN_STACK_NODE_DATA = _ezsp.EZSP_VALUE_TOKEN_STACK_NODE_DATA
EZSP_VALUE_MAC_PASSTHROUGH_FLAGS = _ezsp.EZSP_VALUE_MAC_PASSTHROUGH_FLAGS
EZSP_VALUE_EMBERNET_PASSTHROUGH_SOURCE_ADDRESS = _ezsp.EZSP_VALUE_EMBERNET_PASSTHROUGH_SOURCE_ADDRESS
EZSP_VALUE_FREE_BUFFERS = _ezsp.EZSP_VALUE_FREE_BUFFERS
EZSP_VALUE_UART_SYNCH_CALLBACKS = _ezsp.EZSP_VALUE_UART_SYNCH_CALLBACKS
EZSP_VALUE_MAXIMUM_INCOMING_TRANSFER_SIZE = _ezsp.EZSP_VALUE_MAXIMUM_INCOMING_TRANSFER_SIZE
EZSP_VALUE_MAXIMUM_OUTGOING_TRANSFER_SIZE = _ezsp.EZSP_VALUE_MAXIMUM_OUTGOING_TRANSFER_SIZE
EZSP_VALUE_STACK_TOKEN_WRITING = _ezsp.EZSP_VALUE_STACK_TOKEN_WRITING
EZSP_VALUE_STACK_IS_PERFORMING_REJOIN = _ezsp.EZSP_VALUE_STACK_IS_PERFORMING_REJOIN
EZSP_VALUE_MAC_FILTER_LIST = _ezsp.EZSP_VALUE_MAC_FILTER_LIST
EZSP_VALUE_EXTENDED_SECURITY_BITMASK = _ezsp.EZSP_VALUE_EXTENDED_SECURITY_BITMASK
EZSP_VALUE_NODE_SHORT_ID = _ezsp.EZSP_VALUE_NODE_SHORT_ID
EZSP_VALUE_DESCRIPTOR_CAPABILITY = _ezsp.EZSP_VALUE_DESCRIPTOR_CAPABILITY
EZSP_VALUE_STACK_DEVICE_REQUEST_SEQUENCE_NUMBER = _ezsp.EZSP_VALUE_STACK_DEVICE_REQUEST_SEQUENCE_NUMBER
EZSP_VALUE_RADIO_HOLD_OFF = _ezsp.EZSP_VALUE_RADIO_HOLD_OFF
EZSP_VALUE_ENDPOINT_FLAGS = _ezsp.EZSP_VALUE_ENDPOINT_FLAGS
EZSP_VALUE_MFG_SECURITY_CONFIG = _ezsp.EZSP_VALUE_MFG_SECURITY_CONFIG
EZSP_VALUE_VERSION_INFO = _ezsp.EZSP_VALUE_VERSION_INFO
EZSP_VALUE_NEXT_HOST_REJOIN_REASON = _ezsp.EZSP_VALUE_NEXT_HOST_REJOIN_REASON
EZSP_VALUE_LAST_REJOIN_REASON = _ezsp.EZSP_VALUE_LAST_REJOIN_REASON
EZSP_VALUE_ID_MAX = _ezsp.EZSP_VALUE_ID_MAX
EZSP_EXTENDED_VALUE_ENDPOINT_FLAGS = _ezsp.EZSP_EXTENDED_VALUE_ENDPOINT_FLAGS
EZSP_EXTENDED_VALUE_LAST_LEAVE_REASON = _ezsp.EZSP_EXTENDED_VALUE_LAST_LEAVE_REASON
EZSP_EXTENDED_VALUE_ID_MAX = _ezsp.EZSP_EXTENDED_VALUE_ID_MAX
EZSP_ENDPOINT_DISABLED = _ezsp.EZSP_ENDPOINT_DISABLED
EZSP_ENDPOINT_ENABLED = _ezsp.EZSP_ENDPOINT_ENABLED
EZSP_ENDPOINT_FLAGS_MAX = _ezsp.EZSP_ENDPOINT_FLAGS_MAX
EZSP_TRUST_CENTER_POLICY = _ezsp.EZSP_TRUST_CENTER_POLICY
EZSP_BINDING_MODIFICATION_POLICY = _ezsp.EZSP_BINDING_MODIFICATION_POLICY
EZSP_UNICAST_REPLIES_POLICY = _ezsp.EZSP_UNICAST_REPLIES_POLICY
EZSP_POLL_HANDLER_POLICY = _ezsp.EZSP_POLL_HANDLER_POLICY
EZSP_MESSAGE_CONTENTS_IN_CALLBACK_POLICY = _ezsp.EZSP_MESSAGE_CONTENTS_IN_CALLBACK_POLICY
EZSP_TC_KEY_REQUEST_POLICY = _ezsp.EZSP_TC_KEY_REQUEST_POLICY
EZSP_APP_KEY_REQUEST_POLICY = _ezsp.EZSP_APP_KEY_REQUEST_POLICY
EZSP_PACKET_VALIDATE_LIBRARY_POLICY = _ezsp.EZSP_PACKET_VALIDATE_LIBRARY_POLICY
EZSP_POLICY_ID_MAX = _ezsp.EZSP_POLICY_ID_MAX
EZSP_ALLOW_JOINS = _ezsp.EZSP_ALLOW_JOINS
EZSP_ALLOW_JOINS_REJOINS_HAVE_LINK_KEY = _ezsp.EZSP_ALLOW_JOINS_REJOINS_HAVE_LINK_KEY
EZSP_ALLOW_PRECONFIGURED_KEY_JOINS = _ezsp.EZSP_ALLOW_PRECONFIGURED_KEY_JOINS
EZSP_ALLOW_REJOINS_ONLY = _ezsp.EZSP_ALLOW_REJOINS_ONLY
EZSP_DISALLOW_ALL_JOINS_AND_REJOINS = _ezsp.EZSP_DISALLOW_ALL_JOINS_AND_REJOINS
EZSP_DISALLOW_BINDING_MODIFICATION = _ezsp.EZSP_DISALLOW_BINDING_MODIFICATION
EZSP_ALLOW_BINDING_MODIFICATION = _ezsp.EZSP_ALLOW_BINDING_MODIFICATION
EZSP_CHECK_BINDING_MODIFICATIONS_ARE_VALID_ENDPOINT_CLUSTERS = _ezsp.EZSP_CHECK_BINDING_MODIFICATIONS_ARE_VALID_ENDPOINT_CLUSTERS
EZSP_HOST_WILL_NOT_SUPPLY_REPLY = _ezsp.EZSP_HOST_WILL_NOT_SUPPLY_REPLY
EZSP_HOST_WILL_SUPPLY_REPLY = _ezsp.EZSP_HOST_WILL_SUPPLY_REPLY
EZSP_POLL_HANDLER_IGNORE = _ezsp.EZSP_POLL_HANDLER_IGNORE
EZSP_POLL_HANDLER_CALLBACK = _ezsp.EZSP_POLL_HANDLER_CALLBACK
EZSP_MESSAGE_TAG_ONLY_IN_CALLBACK = _ezsp.EZSP_MESSAGE_TAG_ONLY_IN_CALLBACK
EZSP_MESSAGE_TAG_AND_CONTENTS_IN_CALLBACK = _ezsp.EZSP_MESSAGE_TAG_AND_CONTENTS_IN_CALLBACK
EZSP_DENY_TC_KEY_REQUESTS = _ezsp.EZSP_DENY_TC_KEY_REQUESTS
EZSP_ALLOW_TC_KEY_REQUESTS = _ezsp.EZSP_ALLOW_TC_KEY_REQUESTS
EZSP_DENY_APP_KEY_REQUESTS = _ezsp.EZSP_DENY_APP_KEY_REQUESTS
EZSP_ALLOW_APP_KEY_REQUESTS = _ezsp.EZSP_ALLOW_APP_KEY_REQUESTS
EZSP_PACKET_VALIDATE_LIBRARY_CHECKS_ENABLED = _ezsp.EZSP_PACKET_VALIDATE_LIBRARY_CHECKS_ENABLED
EZSP_PACKET_VALIDATE_LIBRARY_CHECKS_DISABLED = _ezsp.EZSP_PACKET_VALIDATE_LIBRARY_CHECKS_DISABLED
EZSP_DECISION_ID_MAX = _ezsp.EZSP_DECISION_ID_MAX
EZSP_MFG_CUSTOM_VERSION = _ezsp.EZSP_MFG_CUSTOM_VERSION
EZSP_MFG_STRING = _ezsp.EZSP_MFG_STRING
EZSP_MFG_BOARD_NAME = _ezsp.EZSP_MFG_BOARD_NAME
EZSP_MFG_MANUF_ID = _ezsp.EZSP_MFG_MANUF_ID
EZSP_MFG_PHY_CONFIG = _ezsp.EZSP_MFG_PHY_CONFIG
EZSP_MFG_BOOTLOAD_AES_KEY = _ezsp.EZSP_MFG_BOOTLOAD_AES_KEY
EZSP_MFG_ASH_CONFIG = _ezsp.EZSP_MFG_ASH_CONFIG
EZSP_MFG_EZSP_STORAGE = _ezsp.EZSP_MFG_EZSP_STORAGE
EZSP_STACK_CAL_DATA = _ezsp.EZSP_STACK_CAL_DATA
EZSP_MFG_CBKE_DATA = _ezsp.EZSP_MFG_CBKE_DATA
EZSP_MFG_INSTALLATION_CODE = _ezsp.EZSP_MFG_INSTALLATION_CODE
EZSP_STACK_CAL_FILTER = _ezsp.EZSP_STACK_CAL_FILTER
EZSP_MFG_TOKEN_ID_MAX = _ezsp.EZSP_MFG_TOKEN_ID_MAX
EZSP_SUCCESS = _ezsp.EZSP_SUCCESS
EZSP_SPI_ERR_FATAL = _ezsp.EZSP_SPI_ERR_FATAL
EZSP_SPI_ERR_NCP_RESET = _ezsp.EZSP_SPI_ERR_NCP_RESET
EZSP_SPI_ERR_OVERSIZED_EZSP_FRAME = _ezsp.EZSP_SPI_ERR_OVERSIZED_EZSP_FRAME
EZSP_SPI_ERR_ABORTED_TRANSACTION = _ezsp.EZSP_SPI_ERR_ABORTED_TRANSACTION
EZSP_SPI_ERR_MISSING_FRAME_TERMINATOR = _ezsp.EZSP_SPI_ERR_MISSING_FRAME_TERMINATOR
EZSP_SPI_ERR_WAIT_SECTION_TIMEOUT = _ezsp.EZSP_SPI_ERR_WAIT_SECTION_TIMEOUT
EZSP_SPI_ERR_NO_FRAME_TERMINATOR = _ezsp.EZSP_SPI_ERR_NO_FRAME_TERMINATOR
EZSP_SPI_ERR_EZSP_COMMAND_OVERSIZED = _ezsp.EZSP_SPI_ERR_EZSP_COMMAND_OVERSIZED
EZSP_SPI_ERR_EZSP_RESPONSE_OVERSIZED = _ezsp.EZSP_SPI_ERR_EZSP_RESPONSE_OVERSIZED
EZSP_SPI_WAITING_FOR_RESPONSE = _ezsp.EZSP_SPI_WAITING_FOR_RESPONSE
EZSP_SPI_ERR_HANDSHAKE_TIMEOUT = _ezsp.EZSP_SPI_ERR_HANDSHAKE_TIMEOUT
EZSP_SPI_ERR_STARTUP_TIMEOUT = _ezsp.EZSP_SPI_ERR_STARTUP_TIMEOUT
EZSP_SPI_ERR_STARTUP_FAIL = _ezsp.EZSP_SPI_ERR_STARTUP_FAIL
EZSP_SPI_ERR_UNSUPPORTED_SPI_COMMAND = _ezsp.EZSP_SPI_ERR_UNSUPPORTED_SPI_COMMAND
EZSP_ASH_IN_PROGRESS = _ezsp.EZSP_ASH_IN_PROGRESS
EZSP_ASH_HOST_FATAL_ERROR = _ezsp.EZSP_ASH_HOST_FATAL_ERROR
EZSP_ASH_NCP_FATAL_ERROR = _ezsp.EZSP_ASH_NCP_FATAL_ERROR
EZSP_ASH_DATA_FRAME_TOO_LONG = _ezsp.EZSP_ASH_DATA_FRAME_TOO_LONG
EZSP_ASH_DATA_FRAME_TOO_SHORT = _ezsp.EZSP_ASH_DATA_FRAME_TOO_SHORT
EZSP_ASH_NO_TX_SPACE = _ezsp.EZSP_ASH_NO_TX_SPACE
EZSP_ASH_NO_RX_SPACE = _ezsp.EZSP_ASH_NO_RX_SPACE
EZSP_ASH_NO_RX_DATA = _ezsp.EZSP_ASH_NO_RX_DATA
EZSP_ASH_NOT_CONNECTED = _ezsp.EZSP_ASH_NOT_CONNECTED
EZSP_ERROR_VERSION_NOT_SET = _ezsp.EZSP_ERROR_VERSION_NOT_SET
EZSP_ERROR_INVALID_FRAME_ID = _ezsp.EZSP_ERROR_INVALID_FRAME_ID
EZSP_ERROR_WRONG_DIRECTION = _ezsp.EZSP_ERROR_WRONG_DIRECTION
EZSP_ERROR_TRUNCATED = _ezsp.EZSP_ERROR_TRUNCATED
EZSP_ERROR_OVERFLOW = _ezsp.EZSP_ERROR_OVERFLOW
EZSP_ERROR_OUT_OF_MEMORY = _ezsp.EZSP_ERROR_OUT_OF_MEMORY
EZSP_ERROR_INVALID_VALUE = _ezsp.EZSP_ERROR_INVALID_VALUE
EZSP_ERROR_INVALID_ID = _ezsp.EZSP_ERROR_INVALID_ID
EZSP_ERROR_INVALID_CALL = _ezsp.EZSP_ERROR_INVALID_CALL
EZSP_ERROR_NO_RESPONSE = _ezsp.EZSP_ERROR_NO_RESPONSE
EZSP_ERROR_COMMAND_TOO_LONG = _ezsp.EZSP_ERROR_COMMAND_TOO_LONG
EZSP_ERROR_QUEUE_FULL = _ezsp.EZSP_ERROR_QUEUE_FULL
EZSP_ASH_ERROR_VERSION = _ezsp.EZSP_ASH_ERROR_VERSION
EZSP_ASH_ERROR_TIMEOUTS = _ezsp.EZSP_ASH_ERROR_TIMEOUTS
EZSP_ASH_ERROR_RESET_FAIL = _ezsp.EZSP_ASH_ERROR_RESET_FAIL
EZSP_ASH_ERROR_NCP_RESET = _ezsp.EZSP_ASH_ERROR_NCP_RESET
EZSP_ASH_ERROR_SERIAL_INIT = _ezsp.EZSP_ASH_ERROR_SERIAL_INIT
EZSP_ASH_ERROR_NCP_TYPE = _ezsp.EZSP_ASH_ERROR_NCP_TYPE
EZSP_ASH_ERROR_RESET_METHOD = _ezsp.EZSP_ASH_ERROR_RESET_METHOD
EZSP_ASH_ERROR_XON_XOFF = _ezsp.EZSP_ASH_ERROR_XON_XOFF
EZSP_ASH_STARTED = _ezsp.EZSP_ASH_STARTED
EZSP_ASH_CONNECTED = _ezsp.EZSP_ASH_CONNECTED
EZSP_ASH_DISCONNECTED = _ezsp.EZSP_ASH_DISCONNECTED
EZSP_ASH_ACK_TIMEOUT = _ezsp.EZSP_ASH_ACK_TIMEOUT
EZSP_ASH_CANCELLED = _ezsp.EZSP_ASH_CANCELLED
EZSP_ASH_OUT_OF_SEQUENCE = _ezsp.EZSP_ASH_OUT_OF_SEQUENCE
EZSP_ASH_BAD_CRC = _ezsp.EZSP_ASH_BAD_CRC
EZSP_ASH_COMM_ERROR = _ezsp.EZSP_ASH_COMM_ERROR
EZSP_ASH_BAD_ACKNUM = _ezsp.EZSP_ASH_BAD_ACKNUM
EZSP_ASH_TOO_SHORT = _ezsp.EZSP_ASH_TOO_SHORT
EZSP_ASH_TOO_LONG = _ezsp.EZSP_ASH_TOO_LONG
EZSP_ASH_BAD_CONTROL = _ezsp.EZSP_ASH_BAD_CONTROL
EZSP_ASH_BAD_LENGTH = _ezsp.EZSP_ASH_BAD_LENGTH
EZSP_ASH_NO_ERROR = _ezsp.EZSP_ASH_NO_ERROR
EZSP_STATUS_MAX = _ezsp.EZSP_STATUS_MAX
EZSP_ENERGY_SCAN = _ezsp.EZSP_ENERGY_SCAN
EZSP_ACTIVE_SCAN = _ezsp.EZSP_ACTIVE_SCAN
EZSP_NETWORK_SCAN_TYPE_MAX = _ezsp.EZSP_NETWORK_SCAN_TYPE_MAX
EZSP_VERSION = _ezsp.EZSP_VERSION
EZSP_GET_CONFIGURATION_VALUE = _ezsp.EZSP_GET_CONFIGURATION_VALUE
EZSP_SET_CONFIGURATION_VALUE = _ezsp.EZSP_SET_CONFIGURATION_VALUE
EZSP_ADD_ENDPOINT = _ezsp.EZSP_ADD_ENDPOINT
EZSP_SET_POLICY = _ezsp.EZSP_SET_POLICY
EZSP_GET_POLICY = _ezsp.EZSP_GET_POLICY
EZSP_GET_VALUE = _ezsp.EZSP_GET_VALUE
EZSP_GET_EXTENDED_VALUE = _ezsp.EZSP_GET_EXTENDED_VALUE
EZSP_SET_VALUE = _ezsp.EZSP_SET_VALUE
EZSP_SET_GPIO_CURRENT_CONFIGURATION = _ezsp.EZSP_SET_GPIO_CURRENT_CONFIGURATION
EZSP_SET_GPIO_POWER_UP_DOWN_CONFIGURATION = _ezsp.EZSP_SET_GPIO_POWER_UP_DOWN_CONFIGURATION
EZSP_SET_GPIO_RADIO_POWER_MASK = _ezsp.EZSP_SET_GPIO_RADIO_POWER_MASK
EZSP_NOP = _ezsp.EZSP_NOP
EZSP_ECHO = _ezsp.EZSP_ECHO
EZSP_INVALID_COMMAND = _ezsp.EZSP_INVALID_COMMAND
EZSP_CALLBACK = _ezsp.EZSP_CALLBACK
EZSP_NO_CALLBACKS = _ezsp.EZSP_NO_CALLBACKS
EZSP_SET_TOKEN = _ezsp.EZSP_SET_TOKEN
EZSP_GET_TOKEN = _ezsp.EZSP_GET_TOKEN
EZSP_GET_MFG_TOKEN = _ezsp.EZSP_GET_MFG_TOKEN
EZSP_GET_RANDOM_NUMBER = _ezsp.EZSP_GET_RANDOM_NUMBER
EZSP_SET_TIMER = _ezsp.EZSP_SET_TIMER
EZSP_GET_TIMER = _ezsp.EZSP_GET_TIMER
EZSP_TIMER_HANDLER = _ezsp.EZSP_TIMER_HANDLER
EZSP_DEBUG_WRITE = _ezsp.EZSP_DEBUG_WRITE
EZSP_READ_AND_CLEAR_COUNTERS = _ezsp.EZSP_READ_AND_CLEAR_COUNTERS
EZSP_DELAY_TEST = _ezsp.EZSP_DELAY_TEST
EZSP_GET_LIBRARY_STATUS = _ezsp.EZSP_GET_LIBRARY_STATUS
EZSP_SET_MANUFACTURER_CODE = _ezsp.EZSP_SET_MANUFACTURER_CODE
EZSP_SET_POWER_DESCRIPTOR = _ezsp.EZSP_SET_POWER_DESCRIPTOR
EZSP_NETWORK_INIT = _ezsp.EZSP_NETWORK_INIT
EZSP_NETWORK_INIT_EXTENDED = _ezsp.EZSP_NETWORK_INIT_EXTENDED
EZSP_NETWORK_STATE = _ezsp.EZSP_NETWORK_STATE
EZSP_STACK_STATUS_HANDLER = _ezsp.EZSP_STACK_STATUS_HANDLER
EZSP_START_SCAN = _ezsp.EZSP_START_SCAN
EZSP_ENERGY_SCAN_RESULT_HANDLER = _ezsp.EZSP_ENERGY_SCAN_RESULT_HANDLER
EZSP_NETWORK_FOUND_HANDLER = _ezsp.EZSP_NETWORK_FOUND_HANDLER
EZSP_SCAN_COMPLETE_HANDLER = _ezsp.EZSP_SCAN_COMPLETE_HANDLER
EZSP_STOP_SCAN = _ezsp.EZSP_STOP_SCAN
EZSP_FORM_NETWORK = _ezsp.EZSP_FORM_NETWORK
EZSP_JOIN_NETWORK = _ezsp.EZSP_JOIN_NETWORK
EZSP_LEAVE_NETWORK = _ezsp.EZSP_LEAVE_NETWORK
EZSP_FIND_AND_REJOIN_NETWORK = _ezsp.EZSP_FIND_AND_REJOIN_NETWORK
EZSP_PERMIT_JOINING = _ezsp.EZSP_PERMIT_JOINING
EZSP_CHILD_JOIN_HANDLER = _ezsp.EZSP_CHILD_JOIN_HANDLER
EZSP_ENERGY_SCAN_REQUEST = _ezsp.EZSP_ENERGY_SCAN_REQUEST
EZSP_GET_EUI64 = _ezsp.EZSP_GET_EUI64
EZSP_GET_NODE_ID = _ezsp.EZSP_GET_NODE_ID
EZSP_GET_NETWORK_PARAMETERS = _ezsp.EZSP_GET_NETWORK_PARAMETERS
EZSP_GET_PARENT_CHILD_PARAMETERS = _ezsp.EZSP_GET_PARENT_CHILD_PARAMETERS
EZSP_GET_CHILD_DATA = _ezsp.EZSP_GET_CHILD_DATA
EZSP_GET_NEIGHBOR = _ezsp.EZSP_GET_NEIGHBOR
EZSP_NEIGHBOR_COUNT = _ezsp.EZSP_NEIGHBOR_COUNT
EZSP_GET_ROUTE_TABLE_ENTRY = _ezsp.EZSP_GET_ROUTE_TABLE_ENTRY
EZSP_SET_RADIO_POWER = _ezsp.EZSP_SET_RADIO_POWER
EZSP_SET_RADIO_CHANNEL = _ezsp.EZSP_SET_RADIO_CHANNEL
EZSP_CLEAR_BINDING_TABLE = _ezsp.EZSP_CLEAR_BINDING_TABLE
EZSP_SET_BINDING = _ezsp.EZSP_SET_BINDING
EZSP_GET_BINDING = _ezsp.EZSP_GET_BINDING
EZSP_DELETE_BINDING = _ezsp.EZSP_DELETE_BINDING
EZSP_BINDING_IS_ACTIVE = _ezsp.EZSP_BINDING_IS_ACTIVE
EZSP_GET_BINDING_REMOTE_NODE_ID = _ezsp.EZSP_GET_BINDING_REMOTE_NODE_ID
EZSP_SET_BINDING_REMOTE_NODE_ID = _ezsp.EZSP_SET_BINDING_REMOTE_NODE_ID
EZSP_REMOTE_SET_BINDING_HANDLER = _ezsp.EZSP_REMOTE_SET_BINDING_HANDLER
EZSP_REMOTE_DELETE_BINDING_HANDLER = _ezsp.EZSP_REMOTE_DELETE_BINDING_HANDLER
EZSP_MAXIMUM_PAYLOAD_LENGTH = _ezsp.EZSP_MAXIMUM_PAYLOAD_LENGTH
EZSP_SEND_UNICAST = _ezsp.EZSP_SEND_UNICAST
EZSP_SEND_BROADCAST = _ezsp.EZSP_SEND_BROADCAST
EZSP_SEND_MULTICAST = _ezsp.EZSP_SEND_MULTICAST
EZSP_SEND_REPLY = _ezsp.EZSP_SEND_REPLY
EZSP_MESSAGE_SENT_HANDLER = _ezsp.EZSP_MESSAGE_SENT_HANDLER
EZSP_SEND_MANY_TO_ONE_ROUTE_REQUEST = _ezsp.EZSP_SEND_MANY_TO_ONE_ROUTE_REQUEST
EZSP_POLL_FOR_DATA = _ezsp.EZSP_POLL_FOR_DATA
EZSP_POLL_COMPLETE_HANDLER = _ezsp.EZSP_POLL_COMPLETE_HANDLER
EZSP_POLL_HANDLER = _ezsp.EZSP_POLL_HANDLER
EZSP_INCOMING_SENDER_EUI64_HANDLER = _ezsp.EZSP_INCOMING_SENDER_EUI64_HANDLER
EZSP_INCOMING_MESSAGE_HANDLER = _ezsp.EZSP_INCOMING_MESSAGE_HANDLER
EZSP_INCOMING_ROUTE_RECORD_HANDLER = _ezsp.EZSP_INCOMING_ROUTE_RECORD_HANDLER
EZSP_SET_SOURCE_ROUTE = _ezsp.EZSP_SET_SOURCE_ROUTE
EZSP_INCOMING_MANY_TO_ONE_ROUTE_REQUEST_HANDLER = _ezsp.EZSP_INCOMING_MANY_TO_ONE_ROUTE_REQUEST_HANDLER
EZSP_INCOMING_ROUTE_ERROR_HANDLER = _ezsp.EZSP_INCOMING_ROUTE_ERROR_HANDLER
EZSP_ADDRESS_TABLE_ENTRY_IS_ACTIVE = _ezsp.EZSP_ADDRESS_TABLE_ENTRY_IS_ACTIVE
EZSP_SET_ADDRESS_TABLE_REMOTE_EUI64 = _ezsp.EZSP_SET_ADDRESS_TABLE_REMOTE_EUI64
EZSP_SET_ADDRESS_TABLE_REMOTE_NODE_ID = _ezsp.EZSP_SET_ADDRESS_TABLE_REMOTE_NODE_ID
EZSP_GET_ADDRESS_TABLE_REMOTE_EUI64 = _ezsp.EZSP_GET_ADDRESS_TABLE_REMOTE_EUI64
EZSP_GET_ADDRESS_TABLE_REMOTE_NODE_ID = _ezsp.EZSP_GET_ADDRESS_TABLE_REMOTE_NODE_ID
EZSP_SET_EXTENDED_TIMEOUT = _ezsp.EZSP_SET_EXTENDED_TIMEOUT
EZSP_GET_EXTENDED_TIMEOUT = _ezsp.EZSP_GET_EXTENDED_TIMEOUT
EZSP_REPLACE_ADDRESS_TABLE_ENTRY = _ezsp.EZSP_REPLACE_ADDRESS_TABLE_ENTRY
EZSP_LOOKUP_NODE_ID_BY_EUI64 = _ezsp.EZSP_LOOKUP_NODE_ID_BY_EUI64
EZSP_LOOKUP_EUI64_BY_NODE_ID = _ezsp.EZSP_LOOKUP_EUI64_BY_NODE_ID
EZSP_GET_MULTICAST_TABLE_ENTRY = _ezsp.EZSP_GET_MULTICAST_TABLE_ENTRY
EZSP_SET_MULTICAST_TABLE_ENTRY = _ezsp.EZSP_SET_MULTICAST_TABLE_ENTRY
EZSP_ID_CONFLICT_HANDLER = _ezsp.EZSP_ID_CONFLICT_HANDLER
EZSP_SEND_RAW_MESSAGE = _ezsp.EZSP_SEND_RAW_MESSAGE
EZSP_MAC_PASSTHROUGH_MESSAGE_HANDLER = _ezsp.EZSP_MAC_PASSTHROUGH_MESSAGE_HANDLER
EZSP_MAC_FILTER_MATCH_MESSAGE_HANDLER = _ezsp.EZSP_MAC_FILTER_MATCH_MESSAGE_HANDLER
EZSP_RAW_TRANSMIT_COMPLETE_HANDLER = _ezsp.EZSP_RAW_TRANSMIT_COMPLETE_HANDLER
EZSP_SET_INITIAL_SECURITY_STATE = _ezsp.EZSP_SET_INITIAL_SECURITY_STATE
EZSP_GET_CURRENT_SECURITY_STATE = _ezsp.EZSP_GET_CURRENT_SECURITY_STATE
EZSP_GET_KEY = _ezsp.EZSP_GET_KEY
EZSP_SWITCH_NETWORK_KEY_HANDLER = _ezsp.EZSP_SWITCH_NETWORK_KEY_HANDLER
EZSP_GET_KEY_TABLE_ENTRY = _ezsp.EZSP_GET_KEY_TABLE_ENTRY
EZSP_SET_KEY_TABLE_ENTRY = _ezsp.EZSP_SET_KEY_TABLE_ENTRY
EZSP_FIND_KEY_TABLE_ENTRY = _ezsp.EZSP_FIND_KEY_TABLE_ENTRY
EZSP_ADD_OR_UPDATE_KEY_TABLE_ENTRY = _ezsp.EZSP_ADD_OR_UPDATE_KEY_TABLE_ENTRY
EZSP_ERASE_KEY_TABLE_ENTRY = _ezsp.EZSP_ERASE_KEY_TABLE_ENTRY
EZSP_CLEAR_KEY_TABLE = _ezsp.EZSP_CLEAR_KEY_TABLE
EZSP_REQUEST_LINK_KEY = _ezsp.EZSP_REQUEST_LINK_KEY
EZSP_ZIGBEE_KEY_ESTABLISHMENT_HANDLER = _ezsp.EZSP_ZIGBEE_KEY_ESTABLISHMENT_HANDLER
EZSP_TRUST_CENTER_JOIN_HANDLER = _ezsp.EZSP_TRUST_CENTER_JOIN_HANDLER
EZSP_BROADCAST_NEXT_NETWORK_KEY = _ezsp.EZSP_BROADCAST_NEXT_NETWORK_KEY
EZSP_BROADCAST_NETWORK_KEY_SWITCH = _ezsp.EZSP_BROADCAST_NETWORK_KEY_SWITCH
EZSP_BECOME_TRUST_CENTER = _ezsp.EZSP_BECOME_TRUST_CENTER
EZSP_AES_MMO_HASH = _ezsp.EZSP_AES_MMO_HASH
EZSP_REMOVE_DEVICE = _ezsp.EZSP_REMOVE_DEVICE
EZSP_UNICAST_NWK_KEY_UPDATE = _ezsp.EZSP_UNICAST_NWK_KEY_UPDATE
EZSP_GENERATE_CBKE_KEYS = _ezsp.EZSP_GENERATE_CBKE_KEYS
EZSP_GENERATE_CBKE_KEYS_HANDLER = _ezsp.EZSP_GENERATE_CBKE_KEYS_HANDLER
EZSP_CALCULATE_SMACS = _ezsp.EZSP_CALCULATE_SMACS
EZSP_CALCULATE_SMACS_HANDLER = _ezsp.EZSP_CALCULATE_SMACS_HANDLER
EZSP_CLEAR_TEMPORARY_DATA_MAYBE_STORE_LINK_KEY = _ezsp.EZSP_CLEAR_TEMPORARY_DATA_MAYBE_STORE_LINK_KEY
EZSP_GET_CERTIFICATE = _ezsp.EZSP_GET_CERTIFICATE
EZSP_DSA_SIGN = _ezsp.EZSP_DSA_SIGN
EZSP_DSA_SIGN_HANDLER = _ezsp.EZSP_DSA_SIGN_HANDLER
EZSP_DSA_VERIFY = _ezsp.EZSP_DSA_VERIFY
EZSP_DSA_VERIFY_HANDLER = _ezsp.EZSP_DSA_VERIFY_HANDLER
EZSP_SET_PREINSTALLED_CBKE_DATA = _ezsp.EZSP_SET_PREINSTALLED_CBKE_DATA
EZSP_MFGLIB_START = _ezsp.EZSP_MFGLIB_START
EZSP_MFGLIB_END = _ezsp.EZSP_MFGLIB_END
EZSP_MFGLIB_START_TONE = _ezsp.EZSP_MFGLIB_START_TONE
EZSP_MFGLIB_STOP_TONE = _ezsp.EZSP_MFGLIB_STOP_TONE
EZSP_MFGLIB_START_STREAM = _ezsp.EZSP_MFGLIB_START_STREAM
EZSP_MFGLIB_STOP_STREAM = _ezsp.EZSP_MFGLIB_STOP_STREAM
EZSP_MFGLIB_SEND_PACKET = _ezsp.EZSP_MFGLIB_SEND_PACKET
EZSP_MFGLIB_SET_CHANNEL = _ezsp.EZSP_MFGLIB_SET_CHANNEL
EZSP_MFGLIB_GET_CHANNEL = _ezsp.EZSP_MFGLIB_GET_CHANNEL
EZSP_MFGLIB_SET_POWER = _ezsp.EZSP_MFGLIB_SET_POWER
EZSP_MFGLIB_GET_POWER = _ezsp.EZSP_MFGLIB_GET_POWER
EZSP_MFGLIB_RX_HANDLER = _ezsp.EZSP_MFGLIB_RX_HANDLER
EZSP_LAUNCH_STANDALONE_BOOTLOADER = _ezsp.EZSP_LAUNCH_STANDALONE_BOOTLOADER
EZSP_SEND_BOOTLOAD_MESSAGE = _ezsp.EZSP_SEND_BOOTLOAD_MESSAGE
EZSP_GET_STANDALONE_BOOTLOADER_VERSION_PLAT_MICRO_PHY = _ezsp.EZSP_GET_STANDALONE_BOOTLOADER_VERSION_PLAT_MICRO_PHY
EZSP_INCOMING_BOOTLOAD_MESSAGE_HANDLER = _ezsp.EZSP_INCOMING_BOOTLOAD_MESSAGE_HANDLER
EZSP_BOOTLOAD_TRANSMIT_COMPLETE_HANDLER = _ezsp.EZSP_BOOTLOAD_TRANSMIT_COMPLETE_HANDLER
EZSP_AES_ENCRYPT = _ezsp.EZSP_AES_ENCRYPT
EZSP_OVERRIDE_CURRENT_CHANNEL = _ezsp.EZSP_OVERRIDE_CURRENT_CHANNEL
EMBER_SUCCESS = _ezsp.EMBER_SUCCESS
EMBER_ERR_FATAL = _ezsp.EMBER_ERR_FATAL
EMBER_BAD_ARGUMENT = _ezsp.EMBER_BAD_ARGUMENT
EMBER_EEPROM_MFG_STACK_VERSION_MISMATCH = _ezsp.EMBER_EEPROM_MFG_STACK_VERSION_MISMATCH
EMBER_INCOMPATIBLE_STATIC_MEMORY_DEFINITIONS = _ezsp.EMBER_INCOMPATIBLE_STATIC_MEMORY_DEFINITIONS
EMBER_EEPROM_MFG_VERSION_MISMATCH = _ezsp.EMBER_EEPROM_MFG_VERSION_MISMATCH
EMBER_EEPROM_STACK_VERSION_MISMATCH = _ezsp.EMBER_EEPROM_STACK_VERSION_MISMATCH
EMBER_NO_BUFFERS = _ezsp.EMBER_NO_BUFFERS
EMBER_SERIAL_INVALID_BAUD_RATE = _ezsp.EMBER_SERIAL_INVALID_BAUD_RATE
EMBER_SERIAL_INVALID_PORT = _ezsp.EMBER_SERIAL_INVALID_PORT
EMBER_SERIAL_TX_OVERFLOW = _ezsp.EMBER_SERIAL_TX_OVERFLOW
EMBER_SERIAL_RX_OVERFLOW = _ezsp.EMBER_SERIAL_RX_OVERFLOW
EMBER_SERIAL_RX_FRAME_ERROR = _ezsp.EMBER_SERIAL_RX_FRAME_ERROR
EMBER_SERIAL_RX_PARITY_ERROR = _ezsp.EMBER_SERIAL_RX_PARITY_ERROR
EMBER_SERIAL_RX_EMPTY = _ezsp.EMBER_SERIAL_RX_EMPTY
EMBER_SERIAL_RX_OVERRUN_ERROR = _ezsp.EMBER_SERIAL_RX_OVERRUN_ERROR
EMBER_MAC_TRANSMIT_QUEUE_FULL = _ezsp.EMBER_MAC_TRANSMIT_QUEUE_FULL
EMBER_MAC_UNKNOWN_HEADER_TYPE = _ezsp.EMBER_MAC_UNKNOWN_HEADER_TYPE
EMBER_MAC_ACK_HEADER_TYPE = _ezsp.EMBER_MAC_ACK_HEADER_TYPE
EMBER_MAC_SCANNING = _ezsp.EMBER_MAC_SCANNING
EMBER_MAC_NO_DATA = _ezsp.EMBER_MAC_NO_DATA
EMBER_MAC_JOINED_NETWORK = _ezsp.EMBER_MAC_JOINED_NETWORK
EMBER_MAC_BAD_SCAN_DURATION = _ezsp.EMBER_MAC_BAD_SCAN_DURATION
EMBER_MAC_INCORRECT_SCAN_TYPE = _ezsp.EMBER_MAC_INCORRECT_SCAN_TYPE
EMBER_MAC_INVALID_CHANNEL_MASK = _ezsp.EMBER_MAC_INVALID_CHANNEL_MASK
EMBER_MAC_COMMAND_TRANSMIT_FAILURE = _ezsp.EMBER_MAC_COMMAND_TRANSMIT_FAILURE
EMBER_MAC_NO_ACK_RECEIVED = _ezsp.EMBER_MAC_NO_ACK_RECEIVED
EMBER_MAC_RADIO_NETWORK_SWITCH_FAILED = _ezsp.EMBER_MAC_RADIO_NETWORK_SWITCH_FAILED
EMBER_MAC_INDIRECT_TIMEOUT = _ezsp.EMBER_MAC_INDIRECT_TIMEOUT
EMBER_SIM_EEPROM_ERASE_PAGE_GREEN = _ezsp.EMBER_SIM_EEPROM_ERASE_PAGE_GREEN
EMBER_SIM_EEPROM_ERASE_PAGE_RED = _ezsp.EMBER_SIM_EEPROM_ERASE_PAGE_RED
EMBER_SIM_EEPROM_FULL = _ezsp.EMBER_SIM_EEPROM_FULL
EMBER_SIM_EEPROM_INIT_1_FAILED = _ezsp.EMBER_SIM_EEPROM_INIT_1_FAILED
EMBER_SIM_EEPROM_INIT_2_FAILED = _ezsp.EMBER_SIM_EEPROM_INIT_2_FAILED
EMBER_SIM_EEPROM_INIT_3_FAILED = _ezsp.EMBER_SIM_EEPROM_INIT_3_FAILED
EMBER_SIM_EEPROM_REPAIRING = _ezsp.EMBER_SIM_EEPROM_REPAIRING
EMBER_ERR_FLASH_WRITE_INHIBITED = _ezsp.EMBER_ERR_FLASH_WRITE_INHIBITED
EMBER_ERR_FLASH_VERIFY_FAILED = _ezsp.EMBER_ERR_FLASH_VERIFY_FAILED
EMBER_ERR_FLASH_PROG_FAIL = _ezsp.EMBER_ERR_FLASH_PROG_FAIL
EMBER_ERR_FLASH_ERASE_FAIL = _ezsp.EMBER_ERR_FLASH_ERASE_FAIL
EMBER_ERR_BOOTLOADER_TRAP_TABLE_BAD = _ezsp.EMBER_ERR_BOOTLOADER_TRAP_TABLE_BAD
EMBER_ERR_BOOTLOADER_TRAP_UNKNOWN = _ezsp.EMBER_ERR_BOOTLOADER_TRAP_UNKNOWN
EMBER_ERR_BOOTLOADER_NO_IMAGE = _ezsp.EMBER_ERR_BOOTLOADER_NO_IMAGE
EMBER_DELIVERY_FAILED = _ezsp.EMBER_DELIVERY_FAILED
EMBER_BINDING_INDEX_OUT_OF_RANGE = _ezsp.EMBER_BINDING_INDEX_OUT_OF_RANGE
EMBER_ADDRESS_TABLE_INDEX_OUT_OF_RANGE = _ezsp.EMBER_ADDRESS_TABLE_INDEX_OUT_OF_RANGE
EMBER_INVALID_BINDING_INDEX = _ezsp.EMBER_INVALID_BINDING_INDEX
EMBER_INVALID_CALL = _ezsp.EMBER_INVALID_CALL
EMBER_COST_NOT_KNOWN = _ezsp.EMBER_COST_NOT_KNOWN
EMBER_MAX_MESSAGE_LIMIT_REACHED = _ezsp.EMBER_MAX_MESSAGE_LIMIT_REACHED
EMBER_MESSAGE_TOO_LONG = _ezsp.EMBER_MESSAGE_TOO_LONG
EMBER_BINDING_IS_ACTIVE = _ezsp.EMBER_BINDING_IS_ACTIVE
EMBER_ADDRESS_TABLE_ENTRY_IS_ACTIVE = _ezsp.EMBER_ADDRESS_TABLE_ENTRY_IS_ACTIVE
EMBER_ADC_CONVERSION_DONE = _ezsp.EMBER_ADC_CONVERSION_DONE
EMBER_ADC_CONVERSION_BUSY = _ezsp.EMBER_ADC_CONVERSION_BUSY
EMBER_ADC_CONVERSION_DEFERRED = _ezsp.EMBER_ADC_CONVERSION_DEFERRED
EMBER_ADC_NO_CONVERSION_PENDING = _ezsp.EMBER_ADC_NO_CONVERSION_PENDING
EMBER_SLEEP_INTERRUPTED = _ezsp.EMBER_SLEEP_INTERRUPTED
EMBER_PHY_TX_UNDERFLOW = _ezsp.EMBER_PHY_TX_UNDERFLOW
EMBER_PHY_TX_INCOMPLETE = _ezsp.EMBER_PHY_TX_INCOMPLETE
EMBER_PHY_INVALID_CHANNEL = _ezsp.EMBER_PHY_INVALID_CHANNEL
EMBER_PHY_INVALID_POWER = _ezsp.EMBER_PHY_INVALID_POWER
EMBER_PHY_TX_BUSY = _ezsp.EMBER_PHY_TX_BUSY
EMBER_PHY_TX_CCA_FAIL = _ezsp.EMBER_PHY_TX_CCA_FAIL
EMBER_PHY_OSCILLATOR_CHECK_FAILED = _ezsp.EMBER_PHY_OSCILLATOR_CHECK_FAILED
EMBER_PHY_ACK_RECEIVED = _ezsp.EMBER_PHY_ACK_RECEIVED
EMBER_NETWORK_UP = _ezsp.EMBER_NETWORK_UP
EMBER_NETWORK_DOWN = _ezsp.EMBER_NETWORK_DOWN
EMBER_JOIN_FAILED = _ezsp.EMBER_JOIN_FAILED
EMBER_MOVE_FAILED = _ezsp.EMBER_MOVE_FAILED
EMBER_CANNOT_JOIN_AS_ROUTER = _ezsp.EMBER_CANNOT_JOIN_AS_ROUTER
EMBER_NODE_ID_CHANGED = _ezsp.EMBER_NODE_ID_CHANGED
EMBER_PAN_ID_CHANGED = _ezsp.EMBER_PAN_ID_CHANGED
EMBER_CHANNEL_CHANGED = _ezsp.EMBER_CHANNEL_CHANGED
EMBER_NO_BEACONS = _ezsp.EMBER_NO_BEACONS
EMBER_RECEIVED_KEY_IN_THE_CLEAR = _ezsp.EMBER_RECEIVED_KEY_IN_THE_CLEAR
EMBER_NO_NETWORK_KEY_RECEIVED = _ezsp.EMBER_NO_NETWORK_KEY_RECEIVED
EMBER_NO_LINK_KEY_RECEIVED = _ezsp.EMBER_NO_LINK_KEY_RECEIVED
EMBER_PRECONFIGURED_KEY_REQUIRED = _ezsp.EMBER_PRECONFIGURED_KEY_REQUIRED
EMBER_KEY_INVALID = _ezsp.EMBER_KEY_INVALID
EMBER_INVALID_SECURITY_LEVEL = _ezsp.EMBER_INVALID_SECURITY_LEVEL
EMBER_APS_ENCRYPTION_ERROR = _ezsp.EMBER_APS_ENCRYPTION_ERROR
EMBER_TRUST_CENTER_MASTER_KEY_NOT_SET = _ezsp.EMBER_TRUST_CENTER_MASTER_KEY_NOT_SET
EMBER_SECURITY_STATE_NOT_SET = _ezsp.EMBER_SECURITY_STATE_NOT_SET
EMBER_KEY_TABLE_INVALID_ADDRESS = _ezsp.EMBER_KEY_TABLE_INVALID_ADDRESS
EMBER_SECURITY_CONFIGURATION_INVALID = _ezsp.EMBER_SECURITY_CONFIGURATION_INVALID
EMBER_TOO_SOON_FOR_SWITCH_KEY = _ezsp.EMBER_TOO_SOON_FOR_SWITCH_KEY
EMBER_SIGNATURE_VERIFY_FAILURE = _ezsp.EMBER_SIGNATURE_VERIFY_FAILURE
EMBER_KEY_NOT_AUTHORIZED = _ezsp.EMBER_KEY_NOT_AUTHORIZED
EMBER_SECURITY_DATA_INVALID = _ezsp.EMBER_SECURITY_DATA_INVALID
EMBER_NOT_JOINED = _ezsp.EMBER_NOT_JOINED
EMBER_NETWORK_BUSY = _ezsp.EMBER_NETWORK_BUSY
EMBER_INVALID_ENDPOINT = _ezsp.EMBER_INVALID_ENDPOINT
EMBER_BINDING_HAS_CHANGED = _ezsp.EMBER_BINDING_HAS_CHANGED
EMBER_INSUFFICIENT_RANDOM_DATA = _ezsp.EMBER_INSUFFICIENT_RANDOM_DATA
EMBER_SOURCE_ROUTE_FAILURE = _ezsp.EMBER_SOURCE_ROUTE_FAILURE
EMBER_MANY_TO_ONE_ROUTE_FAILURE = _ezsp.EMBER_MANY_TO_ONE_ROUTE_FAILURE
EMBER_STACK_AND_HARDWARE_MISMATCH = _ezsp.EMBER_STACK_AND_HARDWARE_MISMATCH
EMBER_INDEX_OUT_OF_RANGE = _ezsp.EMBER_INDEX_OUT_OF_RANGE
EMBER_TABLE_FULL = _ezsp.EMBER_TABLE_FULL
EMBER_TABLE_ENTRY_ERASED = _ezsp.EMBER_TABLE_ENTRY_ERASED
EMBER_LIBRARY_NOT_PRESENT = _ezsp.EMBER_LIBRARY_NOT_PRESENT
EMBER_OPERATION_IN_PROGRESS = _ezsp.EMBER_OPERATION_IN_PROGRESS
EMBER_TRUST_CENTER_EUI_HAS_CHANGED = _ezsp.EMBER_TRUST_CENTER_EUI_HAS_CHANGED
EMBER_APPLICATION_ERROR_0 = _ezsp.EMBER_APPLICATION_ERROR_0
EMBER_APPLICATION_ERROR_1 = _ezsp.EMBER_APPLICATION_ERROR_1
EMBER_APPLICATION_ERROR_2 = _ezsp.EMBER_APPLICATION_ERROR_2
EMBER_APPLICATION_ERROR_3 = _ezsp.EMBER_APPLICATION_ERROR_3
EMBER_APPLICATION_ERROR_4 = _ezsp.EMBER_APPLICATION_ERROR_4
EMBER_APPLICATION_ERROR_5 = _ezsp.EMBER_APPLICATION_ERROR_5
EMBER_APPLICATION_ERROR_6 = _ezsp.EMBER_APPLICATION_ERROR_6
EMBER_APPLICATION_ERROR_7 = _ezsp.EMBER_APPLICATION_ERROR_7
EMBER_APPLICATION_ERROR_8 = _ezsp.EMBER_APPLICATION_ERROR_8
EMBER_APPLICATION_ERROR_9 = _ezsp.EMBER_APPLICATION_ERROR_9
EMBER_APPLICATION_ERROR_10 = _ezsp.EMBER_APPLICATION_ERROR_10
EMBER_APPLICATION_ERROR_11 = _ezsp.EMBER_APPLICATION_ERROR_11
EMBER_APPLICATION_ERROR_12 = _ezsp.EMBER_APPLICATION_ERROR_12
EMBER_APPLICATION_ERROR_13 = _ezsp.EMBER_APPLICATION_ERROR_13
EMBER_APPLICATION_ERROR_14 = _ezsp.EMBER_APPLICATION_ERROR_14
EMBER_APPLICATION_ERROR_15 = _ezsp.EMBER_APPLICATION_ERROR_15

class EzspStatus(Exception):
    ezspStatusDict = {EZSP_SUCCESS: 'EZSP_SUCCESS',
     EZSP_SPI_ERR_FATAL: 'EZSP_SPI_ERR_FATAL',
     EZSP_SPI_ERR_NCP_RESET: 'EZSP_SPI_ERR_NCP_RESET',
     EZSP_SPI_ERR_OVERSIZED_EZSP_FRAME: 'EZSP_SPI_ERR_OVERSIZED_EZSP_FRAME',
     EZSP_SPI_ERR_ABORTED_TRANSACTION: 'EZSP_SPI_ERR_ABORTED_TRANSACTION',
     EZSP_SPI_ERR_MISSING_FRAME_TERMINATOR: 'EZSP_SPI_ERR_MISSING_FRAME_TERMINATOR',
     EZSP_SPI_ERR_WAIT_SECTION_TIMEOUT: 'EZSP_SPI_ERR_WAIT_SECTION_TIMEOUT',
     EZSP_SPI_ERR_NO_FRAME_TERMINATOR: 'EZSP_SPI_ERR_NO_FRAME_TERMINATOR',
     EZSP_SPI_ERR_EZSP_COMMAND_OVERSIZED: 'EZSP_SPI_ERR_EZSP_COMMAND_OVERSIZED',
     EZSP_SPI_ERR_EZSP_RESPONSE_OVERSIZED: 'EZSP_SPI_ERR_EZSP_RESPONSE_OVERSIZED',
     EZSP_SPI_WAITING_FOR_RESPONSE: 'EZSP_SPI_WAITING_FOR_RESPONSE',
     EZSP_SPI_ERR_HANDSHAKE_TIMEOUT: 'EZSP_SPI_ERR_HANDSHAKE_TIMEOUT',
     EZSP_SPI_ERR_STARTUP_TIMEOUT: 'EZSP_SPI_ERR_STARTUP_TIMEOUT',
     EZSP_SPI_ERR_STARTUP_FAIL: 'EZSP_SPI_ERR_STARTUP_FAIL',
     EZSP_SPI_ERR_UNSUPPORTED_SPI_COMMAND: 'EZSP_SPI_ERR_UNSUPPORTED_SPI_COMMAND',
     EZSP_ASH_IN_PROGRESS: 'EZSP_ASH_IN_PROGRESS',
     EZSP_ASH_HOST_FATAL_ERROR: 'EZSP_ASH_HOST_FATAL_ERROR',
     EZSP_ASH_NCP_FATAL_ERROR: 'EZSP_ASH_NCP_FATAL_ERROR',
     EZSP_ASH_DATA_FRAME_TOO_LONG: 'EZSP_ASH_DATA_FRAME_TOO_LONG',
     EZSP_ASH_DATA_FRAME_TOO_SHORT: 'EZSP_ASH_DATA_FRAME_TOO_SHORT',
     EZSP_ASH_NO_TX_SPACE: 'EZSP_ASH_NO_TX_SPACE',
     EZSP_ASH_NO_RX_SPACE: 'EZSP_ASH_NO_RX_SPACE',
     EZSP_ASH_NO_RX_DATA: 'EZSP_ASH_NO_RX_DATA',
     EZSP_ASH_NOT_CONNECTED: 'EZSP_ASH_NOT_CONNECTED',
     EZSP_ERROR_VERSION_NOT_SET: 'EZSP_ERROR_VERSION_NOT_SET',
     EZSP_ERROR_INVALID_FRAME_ID: 'EZSP_ERROR_INVALID_FRAME_ID',
     EZSP_ERROR_WRONG_DIRECTION: 'EZSP_ERROR_WRONG_DIRECTION',
     EZSP_ERROR_TRUNCATED: 'EZSP_ERROR_TRUNCATED',
     EZSP_ERROR_OVERFLOW: 'EZSP_ERROR_OVERFLOW',
     EZSP_ERROR_OUT_OF_MEMORY: 'EZSP_ERROR_OUT_OF_MEMORY',
     EZSP_ERROR_INVALID_VALUE: 'EZSP_ERROR_INVALID_VALUE',
     EZSP_ERROR_INVALID_ID: 'EZSP_ERROR_INVALID_ID',
     EZSP_ERROR_INVALID_CALL: 'EZSP_ERROR_INVALID_CALL',
     EZSP_ERROR_NO_RESPONSE: 'EZSP_ERROR_NO_RESPONSE',
     EZSP_ERROR_COMMAND_TOO_LONG: 'EZSP_ERROR_COMMAND_TOO_LONG',
     EZSP_ERROR_QUEUE_FULL: 'EZSP_ERROR_QUEUE_FULL',
     EZSP_ASH_ERROR_VERSION: 'EZSP_ASH_ERROR_VERSION',
     EZSP_ASH_ERROR_TIMEOUTS: 'EZSP_ASH_ERROR_TIMEOUTS',
     EZSP_ASH_ERROR_RESET_FAIL: 'EZSP_ASH_ERROR_RESET_FAIL',
     EZSP_ASH_ERROR_NCP_RESET: 'EZSP_ASH_ERROR_NCP_RESET',
     EZSP_ASH_ERROR_SERIAL_INIT: 'EZSP_ASH_ERROR_SERIAL_INIT',
     EZSP_ASH_ERROR_NCP_TYPE: 'EZSP_ASH_ERROR_NCP_TYPE',
     EZSP_ASH_ERROR_RESET_METHOD: 'EZSP_ASH_ERROR_RESET_METHOD',
     EZSP_ASH_ERROR_XON_XOFF: 'EZSP_ASH_ERROR_XON_XOFF',
     EZSP_ASH_STARTED: 'EZSP_ASH_STARTED',
     EZSP_ASH_CONNECTED: 'EZSP_ASH_CONNECTED',
     EZSP_ASH_DISCONNECTED: 'EZSP_ASH_DISCONNECTED',
     EZSP_ASH_ACK_TIMEOUT: 'EZSP_ASH_ACK_TIMEOUT',
     EZSP_ASH_CANCELLED: 'EZSP_ASH_CANCELLED',
     EZSP_ASH_OUT_OF_SEQUENCE: 'EZSP_ASH_OUT_OF_SEQUENCE',
     EZSP_ASH_BAD_CRC: 'EZSP_ASH_BAD_CRC',
     EZSP_ASH_COMM_ERROR: 'EZSP_ASH_COMM_ERROR',
     EZSP_ASH_BAD_ACKNUM: 'EZSP_ASH_BAD_ACKNUM',
     EZSP_ASH_TOO_SHORT: 'EZSP_ASH_TOO_SHORT',
     EZSP_ASH_TOO_LONG: 'EZSP_ASH_TOO_LONG',
     EZSP_ASH_BAD_CONTROL: 'EZSP_ASH_BAD_CONTROL',
     EZSP_ASH_BAD_LENGTH: 'EZSP_ASH_BAD_LENGTH',
     EZSP_ASH_NO_ERROR: 'EZSP_ASH_NO_ERROR'}

    def __init__(self, value, param = 0):
        self.value = value
        self.param = param



    def __repr__(self):
        return '0x%02x' % self.value



    def __str__(self):
        if self.value in self.ezspStatusDict:
            return '%s (0x%02x)' % (self.ezspStatusDict[self.value], self.value)
        else:
            return 'Undefined (0x%02x)' % self.value




class EmberStatus(Exception):
    emberStatusDict = {EMBER_SUCCESS: 'EMBER_SUCCESS',
     EMBER_ERR_FATAL: 'EMBER_ERR_FATAL',
     EMBER_BAD_ARGUMENT: 'EMBER_BAD_ARGUMENT',
     EMBER_EEPROM_MFG_STACK_VERSION_MISMATCH: 'EMBER_EEPROM_MFG_STACK_VERSION_MISMATCH',
     EMBER_INCOMPATIBLE_STATIC_MEMORY_DEFINITIONS: 'EMBER_INCOMPATIBLE_STATIC_MEMORY_DEFINITIONS',
     EMBER_EEPROM_MFG_VERSION_MISMATCH: 'EMBER_EEPROM_MFG_VERSION_MISMATCH',
     EMBER_EEPROM_STACK_VERSION_MISMATCH: 'EMBER_EEPROM_STACK_VERSION_MISMATCH',
     EMBER_NO_BUFFERS: 'EMBER_NO_BUFFERS',
     EMBER_SERIAL_INVALID_BAUD_RATE: 'EMBER_SERIAL_INVALID_BAUD_RATE',
     EMBER_SERIAL_INVALID_PORT: 'EMBER_SERIAL_INVALID_PORT',
     EMBER_SERIAL_TX_OVERFLOW: 'EMBER_SERIAL_TX_OVERFLOW',
     EMBER_SERIAL_RX_OVERFLOW: 'EMBER_SERIAL_RX_OVERFLOW',
     EMBER_SERIAL_RX_FRAME_ERROR: 'EMBER_SERIAL_RX_FRAME_ERROR',
     EMBER_SERIAL_RX_PARITY_ERROR: 'EMBER_SERIAL_RX_PARITY_ERROR',
     EMBER_SERIAL_RX_EMPTY: 'EMBER_SERIAL_RX_EMPTY',
     EMBER_SERIAL_RX_OVERRUN_ERROR: 'EMBER_SERIAL_RX_OVERRUN_ERROR',
     EMBER_MAC_TRANSMIT_QUEUE_FULL: 'EMBER_MAC_TRANSMIT_QUEUE_FULL',
     EMBER_MAC_UNKNOWN_HEADER_TYPE: 'EMBER_MAC_UNKNOWN_HEADER_TYPE',
     EMBER_MAC_ACK_HEADER_TYPE: 'EMBER_MAC_ACK_HEADER_TYPE',
     EMBER_MAC_SCANNING: 'EMBER_MAC_SCANNING',
     EMBER_MAC_NO_DATA: 'EMBER_MAC_NO_DATA',
     EMBER_MAC_JOINED_NETWORK: 'EMBER_MAC_JOINED_NETWORK',
     EMBER_MAC_BAD_SCAN_DURATION: 'EMBER_MAC_BAD_SCAN_DURATION',
     EMBER_MAC_INCORRECT_SCAN_TYPE: 'EMBER_MAC_INCORRECT_SCAN_TYPE',
     EMBER_MAC_INVALID_CHANNEL_MASK: 'EMBER_MAC_INVALID_CHANNEL_MASK',
     EMBER_MAC_COMMAND_TRANSMIT_FAILURE: 'EMBER_MAC_COMMAND_TRANSMIT_FAILURE',
     EMBER_MAC_NO_ACK_RECEIVED: 'EMBER_MAC_NO_ACK_RECEIVED',
     EMBER_MAC_RADIO_NETWORK_SWITCH_FAILED: 'EMBER_MAC_RADIO_NETWORK_SWITCH_FAILED',
     EMBER_MAC_INDIRECT_TIMEOUT: 'EMBER_MAC_INDIRECT_TIMEOUT',
     EMBER_SIM_EEPROM_ERASE_PAGE_GREEN: 'EMBER_SIM_EEPROM_ERASE_PAGE_GREEN',
     EMBER_SIM_EEPROM_ERASE_PAGE_RED: 'EMBER_SIM_EEPROM_ERASE_PAGE_RED',
     EMBER_SIM_EEPROM_FULL: 'EMBER_SIM_EEPROM_FULL',
     EMBER_SIM_EEPROM_INIT_1_FAILED: 'EMBER_SIM_EEPROM_INIT_1_FAILED',
     EMBER_SIM_EEPROM_INIT_2_FAILED: 'EMBER_SIM_EEPROM_INIT_2_FAILED',
     EMBER_SIM_EEPROM_INIT_3_FAILED: 'EMBER_SIM_EEPROM_INIT_3_FAILED',
     EMBER_SIM_EEPROM_REPAIRING: 'EMBER_SIM_EEPROM_REPAIRING',
     EMBER_ERR_FLASH_WRITE_INHIBITED: 'EMBER_ERR_FLASH_WRITE_INHIBITED',
     EMBER_ERR_FLASH_VERIFY_FAILED: 'EMBER_ERR_FLASH_VERIFY_FAILED',
     EMBER_ERR_FLASH_PROG_FAIL: 'EMBER_ERR_FLASH_PROG_FAIL',
     EMBER_ERR_FLASH_ERASE_FAIL: 'EMBER_ERR_FLASH_ERASE_FAIL',
     EMBER_ERR_BOOTLOADER_TRAP_TABLE_BAD: 'EMBER_ERR_BOOTLOADER_TRAP_TABLE_BAD',
     EMBER_ERR_BOOTLOADER_TRAP_UNKNOWN: 'EMBER_ERR_BOOTLOADER_TRAP_UNKNOWN',
     EMBER_ERR_BOOTLOADER_NO_IMAGE: 'EMBER_ERR_BOOTLOADER_NO_IMAGE',
     EMBER_DELIVERY_FAILED: 'EMBER_DELIVERY_FAILED',
     EMBER_BINDING_INDEX_OUT_OF_RANGE: 'EMBER_BINDING_INDEX_OUT_OF_RANGE',
     EMBER_ADDRESS_TABLE_INDEX_OUT_OF_RANGE: 'EMBER_ADDRESS_TABLE_INDEX_OUT_OF_RANGE',
     EMBER_INVALID_BINDING_INDEX: 'EMBER_INVALID_BINDING_INDEX',
     EMBER_INVALID_CALL: 'EMBER_INVALID_CALL',
     EMBER_COST_NOT_KNOWN: 'EMBER_COST_NOT_KNOWN',
     EMBER_MAX_MESSAGE_LIMIT_REACHED: 'EMBER_MAX_MESSAGE_LIMIT_REACHED',
     EMBER_MESSAGE_TOO_LONG: 'EMBER_MESSAGE_TOO_LONG',
     EMBER_BINDING_IS_ACTIVE: 'EMBER_BINDING_IS_ACTIVE',
     EMBER_ADDRESS_TABLE_ENTRY_IS_ACTIVE: 'EMBER_ADDRESS_TABLE_ENTRY_IS_ACTIVE',
     EMBER_ADC_CONVERSION_DONE: 'EMBER_ADC_CONVERSION_DONE',
     EMBER_ADC_CONVERSION_BUSY: 'EMBER_ADC_CONVERSION_BUSY',
     EMBER_ADC_CONVERSION_DEFERRED: 'EMBER_ADC_CONVERSION_DEFERRED',
     EMBER_ADC_NO_CONVERSION_PENDING: 'EMBER_ADC_NO_CONVERSION_PENDING',
     EMBER_SLEEP_INTERRUPTED: 'EMBER_SLEEP_INTERRUPTED',
     EMBER_PHY_TX_UNDERFLOW: 'EMBER_PHY_TX_UNDERFLOW',
     EMBER_PHY_TX_INCOMPLETE: 'EMBER_PHY_TX_INCOMPLETE',
     EMBER_PHY_INVALID_CHANNEL: 'EMBER_PHY_INVALID_CHANNEL',
     EMBER_PHY_INVALID_POWER: 'EMBER_PHY_INVALID_POWER',
     EMBER_PHY_TX_BUSY: 'EMBER_PHY_TX_BUSY',
     EMBER_PHY_TX_CCA_FAIL: 'EMBER_PHY_TX_CCA_FAIL',
     EMBER_PHY_OSCILLATOR_CHECK_FAILED: 'EMBER_PHY_OSCILLATOR_CHECK_FAILED',
     EMBER_PHY_ACK_RECEIVED: 'EMBER_PHY_ACK_RECEIVED',
     EMBER_NETWORK_UP: 'EMBER_NETWORK_UP',
     EMBER_NETWORK_DOWN: 'EMBER_NETWORK_DOWN',
     EMBER_JOIN_FAILED: 'EMBER_JOIN_FAILED',
     EMBER_MOVE_FAILED: 'EMBER_MOVE_FAILED',
     EMBER_CANNOT_JOIN_AS_ROUTER: 'EMBER_CANNOT_JOIN_AS_ROUTER',
     EMBER_NODE_ID_CHANGED: 'EMBER_NODE_ID_CHANGED',
     EMBER_PAN_ID_CHANGED: 'EMBER_PAN_ID_CHANGED',
     EMBER_CHANNEL_CHANGED: 'EMBER_CHANNEL_CHANGED',
     EMBER_NO_BEACONS: 'EMBER_NO_BEACONS',
     EMBER_RECEIVED_KEY_IN_THE_CLEAR: 'EMBER_RECEIVED_KEY_IN_THE_CLEAR',
     EMBER_NO_NETWORK_KEY_RECEIVED: 'EMBER_NO_NETWORK_KEY_RECEIVED',
     EMBER_NO_LINK_KEY_RECEIVED: 'EMBER_NO_LINK_KEY_RECEIVED',
     EMBER_PRECONFIGURED_KEY_REQUIRED: 'EMBER_PRECONFIGURED_KEY_REQUIRED',
     EMBER_KEY_INVALID: 'EMBER_KEY_INVALID',
     EMBER_INVALID_SECURITY_LEVEL: 'EMBER_INVALID_SECURITY_LEVEL',
     EMBER_APS_ENCRYPTION_ERROR: 'EMBER_APS_ENCRYPTION_ERROR',
     EMBER_TRUST_CENTER_MASTER_KEY_NOT_SET: 'EMBER_TRUST_CENTER_MASTER_KEY_NOT_SET',
     EMBER_SECURITY_STATE_NOT_SET: 'EMBER_SECURITY_STATE_NOT_SET',
     EMBER_KEY_TABLE_INVALID_ADDRESS: 'EMBER_KEY_TABLE_INVALID_ADDRESS',
     EMBER_SECURITY_CONFIGURATION_INVALID: 'EMBER_SECURITY_CONFIGURATION_INVALID',
     EMBER_TOO_SOON_FOR_SWITCH_KEY: 'EMBER_TOO_SOON_FOR_SWITCH_KEY',
     EMBER_SIGNATURE_VERIFY_FAILURE: 'EMBER_SIGNATURE_VERIFY_FAILURE',
     EMBER_KEY_NOT_AUTHORIZED: 'EMBER_KEY_NOT_AUTHORIZED',
     EMBER_SECURITY_DATA_INVALID: 'EMBER_SECURITY_DATA_INVALID',
     EMBER_NOT_JOINED: 'EMBER_NOT_JOINED',
     EMBER_NETWORK_BUSY: 'EMBER_NETWORK_BUSY',
     EMBER_INVALID_ENDPOINT: 'EMBER_INVALID_ENDPOINT',
     EMBER_BINDING_HAS_CHANGED: 'EMBER_BINDING_HAS_CHANGED',
     EMBER_INSUFFICIENT_RANDOM_DATA: 'EMBER_INSUFFICIENT_RANDOM_DATA',
     EMBER_SOURCE_ROUTE_FAILURE: 'EMBER_SOURCE_ROUTE_FAILURE',
     EMBER_MANY_TO_ONE_ROUTE_FAILURE: 'EMBER_MANY_TO_ONE_ROUTE_FAILURE',
     EMBER_STACK_AND_HARDWARE_MISMATCH: 'EMBER_STACK_AND_HARDWARE_MISMATCH',
     EMBER_INDEX_OUT_OF_RANGE: 'EMBER_INDEX_OUT_OF_RANGE',
     EMBER_TABLE_FULL: 'EMBER_TABLE_FULL',
     EMBER_TABLE_ENTRY_ERASED: 'EMBER_TABLE_ENTRY_ERASED',
     EMBER_LIBRARY_NOT_PRESENT: 'EMBER_LIBRARY_NOT_PRESENT',
     EMBER_OPERATION_IN_PROGRESS: 'EMBER_OPERATION_IN_PROGRESS',
     EMBER_TRUST_CENTER_EUI_HAS_CHANGED: 'EMBER_TRUST_CENTER_EUI_HAS_CHANGED',
     EMBER_APPLICATION_ERROR_0: 'EMBER_APPLICATION_ERROR_0',
     EMBER_APPLICATION_ERROR_1: 'EMBER_APPLICATION_ERROR_1',
     EMBER_APPLICATION_ERROR_2: 'EMBER_APPLICATION_ERROR_2',
     EMBER_APPLICATION_ERROR_3: 'EMBER_APPLICATION_ERROR_3',
     EMBER_APPLICATION_ERROR_4: 'EMBER_APPLICATION_ERROR_4',
     EMBER_APPLICATION_ERROR_5: 'EMBER_APPLICATION_ERROR_5',
     EMBER_APPLICATION_ERROR_6: 'EMBER_APPLICATION_ERROR_6',
     EMBER_APPLICATION_ERROR_7: 'EMBER_APPLICATION_ERROR_7',
     EMBER_APPLICATION_ERROR_8: 'EMBER_APPLICATION_ERROR_8',
     EMBER_APPLICATION_ERROR_9: 'EMBER_APPLICATION_ERROR_9',
     EMBER_APPLICATION_ERROR_10: 'EMBER_APPLICATION_ERROR_10',
     EMBER_APPLICATION_ERROR_11: 'EMBER_APPLICATION_ERROR_11',
     EMBER_APPLICATION_ERROR_12: 'EMBER_APPLICATION_ERROR_12',
     EMBER_APPLICATION_ERROR_13: 'EMBER_APPLICATION_ERROR_13',
     EMBER_APPLICATION_ERROR_14: 'EMBER_APPLICATION_ERROR_14',
     EMBER_APPLICATION_ERROR_15: 'EMBER_APPLICATION_ERROR_15'}

    def __init__(self, value, param = 0):
        self.value = value
        self.param = param



    def __repr__(self):
        return '0x%02x' % self.value



    def __str__(self):
        if self.value in self.emberStatusDict:
            return '%s (0x%02x)' % (self.emberStatusDict[self.value], self.value)
        else:
            return 'Undefined (0x%02x)' % self.value




class EZSPInterface(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, EZSPInterface, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, EZSPInterface, name)
    __repr__ = _swig_repr

    def ezspVersion(self, *args):
        return _ezsp.EZSPInterface_ezspVersion(self, *args)



    def ezspGetConfigurationValue(self, *args):
        return _ezsp.EZSPInterface_ezspGetConfigurationValue(self, *args)



    def ezspSetConfigurationValue(self, *args):
        return _ezsp.EZSPInterface_ezspSetConfigurationValue(self, *args)



    def ezspAddEndpoint(self, *args):
        return _ezsp.EZSPInterface_ezspAddEndpoint(self, *args)



    def ezspSetPolicy(self, *args):
        return _ezsp.EZSPInterface_ezspSetPolicy(self, *args)



    def ezspGetPolicy(self, *args):
        return _ezsp.EZSPInterface_ezspGetPolicy(self, *args)



    def ezspGetValue(self, *args):
        return _ezsp.EZSPInterface_ezspGetValue(self, *args)



    def ezspGetExtendedValue(self, *args):
        return _ezsp.EZSPInterface_ezspGetExtendedValue(self, *args)



    def ezspSetValue(self, *args):
        return _ezsp.EZSPInterface_ezspSetValue(self, *args)



    def ezspSetGpioCurrentConfiguration(self, *args):
        return _ezsp.EZSPInterface_ezspSetGpioCurrentConfiguration(self, *args)



    def ezspSetGpioPowerUpDownConfiguration(self, *args):
        return _ezsp.EZSPInterface_ezspSetGpioPowerUpDownConfiguration(self, *args)



    def ezspSetGpioRadioPowerMask(self, *args):
        return _ezsp.EZSPInterface_ezspSetGpioRadioPowerMask(self, *args)



    def ezspNop(self):
        return _ezsp.EZSPInterface_ezspNop(self)



    def ezspEcho(self, *args):
        return _ezsp.EZSPInterface_ezspEcho(self, *args)



    def ezspCallback(self):
        return _ezsp.EZSPInterface_ezspCallback(self)



    def ezspSetToken(self, *args):
        return _ezsp.EZSPInterface_ezspSetToken(self, *args)



    def ezspGetToken(self, *args):
        return _ezsp.EZSPInterface_ezspGetToken(self, *args)



    def ezspGetRandomNumber(self):
        return _ezsp.EZSPInterface_ezspGetRandomNumber(self)



    def ezspSetTimer(self, *args):
        return _ezsp.EZSPInterface_ezspSetTimer(self, *args)



    def ezspGetTimer(self, *args):
        return _ezsp.EZSPInterface_ezspGetTimer(self, *args)



    def ezspDebugWrite(self, *args):
        return _ezsp.EZSPInterface_ezspDebugWrite(self, *args)



    def ezspReadAndClearCounters(self):
        return _ezsp.EZSPInterface_ezspReadAndClearCounters(self)



    def ezspDelayTest(self, *args):
        return _ezsp.EZSPInterface_ezspDelayTest(self, *args)



    def emberGetLibraryStatus(self, *args):
        return _ezsp.EZSPInterface_emberGetLibraryStatus(self, *args)



    def emberSetManufacturerCode(self, *args):
        return _ezsp.EZSPInterface_emberSetManufacturerCode(self, *args)



    def emberSetPowerDescriptor(self, *args):
        return _ezsp.EZSPInterface_emberSetPowerDescriptor(self, *args)



    def emberNetworkInit(self):
        return _ezsp.EZSPInterface_emberNetworkInit(self)



    def emberNetworkInitExtended(self, *args):
        return _ezsp.EZSPInterface_emberNetworkInitExtended(self, *args)



    def emberNetworkState(self):
        return _ezsp.EZSPInterface_emberNetworkState(self)



    def emberStartScan(self, *args):
        return _ezsp.EZSPInterface_emberStartScan(self, *args)



    def emberStopScan(self):
        return _ezsp.EZSPInterface_emberStopScan(self)



    def emberFormNetwork(self, *args):
        return _ezsp.EZSPInterface_emberFormNetwork(self, *args)



    def emberJoinNetwork(self, *args):
        return _ezsp.EZSPInterface_emberJoinNetwork(self, *args)



    def emberLeaveNetwork(self):
        return _ezsp.EZSPInterface_emberLeaveNetwork(self)



    def emberFindAndRejoinNetwork(self, *args):
        return _ezsp.EZSPInterface_emberFindAndRejoinNetwork(self, *args)



    def emberPermitJoining(self, *args):
        return _ezsp.EZSPInterface_emberPermitJoining(self, *args)



    def emberEnergyScanRequest(self, *args):
        return _ezsp.EZSPInterface_emberEnergyScanRequest(self, *args)



    def ezspGetEui64(self):
        return _ezsp.EZSPInterface_ezspGetEui64(self)



    def emberGetNodeId(self):
        return _ezsp.EZSPInterface_emberGetNodeId(self)



    def ezspGetNetworkParameters(self, *args):
        return _ezsp.EZSPInterface_ezspGetNetworkParameters(self, *args)



    def ezspGetParentChildParameters(self):
        return _ezsp.EZSPInterface_ezspGetParentChildParameters(self)



    def ezspGetChildData(self, *args):
        return _ezsp.EZSPInterface_ezspGetChildData(self, *args)



    def emberGetNeighbor(self, *args):
        return _ezsp.EZSPInterface_emberGetNeighbor(self, *args)



    def emberNeighborCount(self):
        return _ezsp.EZSPInterface_emberNeighborCount(self)



    def emberGetRouteTableEntry(self, *args):
        return _ezsp.EZSPInterface_emberGetRouteTableEntry(self, *args)



    def emberSetRadioPower(self, *args):
        return _ezsp.EZSPInterface_emberSetRadioPower(self, *args)



    def emberSetRadioChannel(self, *args):
        return _ezsp.EZSPInterface_emberSetRadioChannel(self, *args)



    def emberClearBindingTable(self):
        return _ezsp.EZSPInterface_emberClearBindingTable(self)



    def emberSetBinding(self, *args):
        return _ezsp.EZSPInterface_emberSetBinding(self, *args)



    def emberGetBinding(self, *args):
        return _ezsp.EZSPInterface_emberGetBinding(self, *args)



    def emberDeleteBinding(self, *args):
        return _ezsp.EZSPInterface_emberDeleteBinding(self, *args)



    def emberBindingIsActive(self, *args):
        return _ezsp.EZSPInterface_emberBindingIsActive(self, *args)



    def emberGetBindingRemoteNodeId(self, *args):
        return _ezsp.EZSPInterface_emberGetBindingRemoteNodeId(self, *args)



    def emberSetBindingRemoteNodeId(self, *args):
        return _ezsp.EZSPInterface_emberSetBindingRemoteNodeId(self, *args)



    def ezspMaximumPayloadLength(self):
        return _ezsp.EZSPInterface_ezspMaximumPayloadLength(self)



    def ezspSendUnicast(self, *args):
        return _ezsp.EZSPInterface_ezspSendUnicast(self, *args)



    def ezspSendBroadcast(self, *args):
        return _ezsp.EZSPInterface_ezspSendBroadcast(self, *args)



    def ezspSendMulticast(self, *args):
        return _ezsp.EZSPInterface_ezspSendMulticast(self, *args)



    def ezspSendReply(self, *args):
        return _ezsp.EZSPInterface_ezspSendReply(self, *args)



    def emberSendManyToOneRouteRequest(self, *args):
        return _ezsp.EZSPInterface_emberSendManyToOneRouteRequest(self, *args)



    def ezspPollForData(self, *args):
        return _ezsp.EZSPInterface_ezspPollForData(self, *args)



    def ezspSetSourceRoute(self, *args):
        return _ezsp.EZSPInterface_ezspSetSourceRoute(self, *args)



    def emberAddressTableEntryIsActive(self, *args):
        return _ezsp.EZSPInterface_emberAddressTableEntryIsActive(self, *args)



    def emberSetAddressTableRemoteEui64(self, *args):
        return _ezsp.EZSPInterface_emberSetAddressTableRemoteEui64(self, *args)



    def emberSetAddressTableRemoteNodeId(self, *args):
        return _ezsp.EZSPInterface_emberSetAddressTableRemoteNodeId(self, *args)



    def emberGetAddressTableRemoteEui64(self, *args):
        return _ezsp.EZSPInterface_emberGetAddressTableRemoteEui64(self, *args)



    def emberGetAddressTableRemoteNodeId(self, *args):
        return _ezsp.EZSPInterface_emberGetAddressTableRemoteNodeId(self, *args)



    def emberSetExtendedTimeout(self, *args):
        return _ezsp.EZSPInterface_emberSetExtendedTimeout(self, *args)



    def emberGetExtendedTimeout(self, *args):
        return _ezsp.EZSPInterface_emberGetExtendedTimeout(self, *args)



    def ezspReplaceAddressTableEntry(self, *args):
        return _ezsp.EZSPInterface_ezspReplaceAddressTableEntry(self, *args)



    def emberLookupNodeIdByEui64(self, *args):
        return _ezsp.EZSPInterface_emberLookupNodeIdByEui64(self, *args)



    def emberLookupEui64ByNodeId(self, *args):
        return _ezsp.EZSPInterface_emberLookupEui64ByNodeId(self, *args)



    def ezspGetMulticastTableEntry(self, *args):
        return _ezsp.EZSPInterface_ezspGetMulticastTableEntry(self, *args)



    def ezspSetMulticastTableEntry(self, *args):
        return _ezsp.EZSPInterface_ezspSetMulticastTableEntry(self, *args)



    def ezspSendRawMessage(self, *args):
        return _ezsp.EZSPInterface_ezspSendRawMessage(self, *args)



    def emberSetInitialSecurityState(self, *args):
        return _ezsp.EZSPInterface_emberSetInitialSecurityState(self, *args)



    def emberGetCurrentSecurityState(self, *args):
        return _ezsp.EZSPInterface_emberGetCurrentSecurityState(self, *args)



    def emberGetKey(self, *args):
        return _ezsp.EZSPInterface_emberGetKey(self, *args)



    def emberGetKeyTableEntry(self, *args):
        return _ezsp.EZSPInterface_emberGetKeyTableEntry(self, *args)



    def emberSetKeyTableEntry(self, *args):
        return _ezsp.EZSPInterface_emberSetKeyTableEntry(self, *args)



    def emberFindKeyTableEntry(self, *args):
        return _ezsp.EZSPInterface_emberFindKeyTableEntry(self, *args)



    def emberAddOrUpdateKeyTableEntry(self, *args):
        return _ezsp.EZSPInterface_emberAddOrUpdateKeyTableEntry(self, *args)



    def emberEraseKeyTableEntry(self, *args):
        return _ezsp.EZSPInterface_emberEraseKeyTableEntry(self, *args)



    def emberClearKeyTable(self):
        return _ezsp.EZSPInterface_emberClearKeyTable(self)



    def emberRequestLinkKey(self, *args):
        return _ezsp.EZSPInterface_emberRequestLinkKey(self, *args)



    def emberBroadcastNextNetworkKey(self, *args):
        return _ezsp.EZSPInterface_emberBroadcastNextNetworkKey(self, *args)



    def emberBroadcastNetworkKeySwitch(self):
        return _ezsp.EZSPInterface_emberBroadcastNetworkKeySwitch(self)



    def emberBecomeTrustCenter(self, *args):
        return _ezsp.EZSPInterface_emberBecomeTrustCenter(self, *args)



    def ezspRemoveDevice(self, *args):
        return _ezsp.EZSPInterface_ezspRemoveDevice(self, *args)



    def ezspUnicastNwkKeyUpdate(self, *args):
        return _ezsp.EZSPInterface_ezspUnicastNwkKeyUpdate(self, *args)



    def emberGenerateCbkeKeys(self):
        return _ezsp.EZSPInterface_emberGenerateCbkeKeys(self)



    def emberCalculateSmacs(self, *args):
        return _ezsp.EZSPInterface_emberCalculateSmacs(self, *args)



    def emberClearTemporaryDataMaybeStoreLinkKey(self, *args):
        return _ezsp.EZSPInterface_emberClearTemporaryDataMaybeStoreLinkKey(self, *args)



    def emberGetCertificate(self, *args):
        return _ezsp.EZSPInterface_emberGetCertificate(self, *args)



    def emberDsaVerify(self, *args):
        return _ezsp.EZSPInterface_emberDsaVerify(self, *args)



    def emberSetPreinstalledCbkeData(self, *args):
        return _ezsp.EZSPInterface_emberSetPreinstalledCbkeData(self, *args)



    def ezspMfglibStart(self, *args):
        return _ezsp.EZSPInterface_ezspMfglibStart(self, *args)



    def mfglibEnd(self):
        return _ezsp.EZSPInterface_mfglibEnd(self)



    def mfglibStartTone(self):
        return _ezsp.EZSPInterface_mfglibStartTone(self)



    def mfglibStopTone(self):
        return _ezsp.EZSPInterface_mfglibStopTone(self)



    def mfglibStartStream(self):
        return _ezsp.EZSPInterface_mfglibStartStream(self)



    def mfglibStopStream(self):
        return _ezsp.EZSPInterface_mfglibStopStream(self)



    def mfglibSendPacket(self, *args):
        return _ezsp.EZSPInterface_mfglibSendPacket(self, *args)



    def mfglibSetChannel(self, *args):
        return _ezsp.EZSPInterface_mfglibSetChannel(self, *args)



    def mfglibGetChannel(self):
        return _ezsp.EZSPInterface_mfglibGetChannel(self)



    def mfglibSetPower(self, *args):
        return _ezsp.EZSPInterface_mfglibSetPower(self, *args)



    def mfglibGetPower(self):
        return _ezsp.EZSPInterface_mfglibGetPower(self)



    def ezspLaunchStandaloneBootloader(self, *args):
        return _ezsp.EZSPInterface_ezspLaunchStandaloneBootloader(self, *args)



    def ezspSendBootloadMessage(self, *args):
        return _ezsp.EZSPInterface_ezspSendBootloadMessage(self, *args)



    def ezspGetStandaloneBootloaderVersionPlatMicroPhy(self):
        return _ezsp.EZSPInterface_ezspGetStandaloneBootloaderVersionPlatMicroPhy(self)



    def ezspAesEncrypt(self, *args):
        return _ezsp.EZSPInterface_ezspAesEncrypt(self, *args)



    def ezspOverrideCurrentChannel(self, *args):
        return _ezsp.EZSPInterface_ezspOverrideCurrentChannel(self, *args)



    def XModemQuery(self, *args):
        return _ezsp.EZSPInterface_XModemQuery(self, *args)



    def bootSendMessage(self, *args):
        return _ezsp.EZSPInterface_bootSendMessage(self, *args)



    def waitFor260boot(self):
        return _ezsp.EZSPInterface_waitFor260boot(self)



    def XModemPollForResult(self, *args):
        return _ezsp.EZSPInterface_XModemPollForResult(self, *args)



    def ezspGetVersionStruct(self, *args):
        return _ezsp.EZSPInterface_ezspGetVersionStruct(self, *args)



    def ezspSetEndpointFlags(self, *args):
        return _ezsp.EZSPInterface_ezspSetEndpointFlags(self, *args)



    def ezspGetEndpointFlags(self, *args):
        return _ezsp.EZSPInterface_ezspGetEndpointFlags(self, *args)



    def ezspEnableEndpoint(self, *args):
        return _ezsp.EZSPInterface_ezspEnableEndpoint(self, *args)



    def emberStackIsPerformingRejoin(self):
        return _ezsp.EZSPInterface_emberStackIsPerformingRejoin(self)



    def emberSetMfgSecurityConfig(self, *args):
        return _ezsp.EZSPInterface_emberSetMfgSecurityConfig(self, *args)



    def emberGetMfgSecurityConfig(self, *args):
        return _ezsp.EZSPInterface_emberGetMfgSecurityConfig(self, *args)



    def emberStartWritingStackTokens(self):
        return _ezsp.EZSPInterface_emberStartWritingStackTokens(self)



    def emberStopWritingStackTokens(self):
        return _ezsp.EZSPInterface_emberStopWritingStackTokens(self)



    def emberWritingStackTokensEnabled(self):
        return _ezsp.EZSPInterface_emberWritingStackTokensEnabled(self)



    def emberSetExtendedSecurityBitmask(self, *args):
        return _ezsp.EZSPInterface_emberSetExtendedSecurityBitmask(self, *args)



    def emberGetExtendedSecurityBitmask(self, *args):
        return _ezsp.EZSPInterface_emberGetExtendedSecurityBitmask(self, *args)



    def emberSetNodeId(self, *args):
        return _ezsp.EZSPInterface_emberSetNodeId(self, *args)



    def emberSetMaximumIncomingTransferSize(self, *args):
        return _ezsp.EZSPInterface_emberSetMaximumIncomingTransferSize(self, *args)



    def emberSetMaximumOutgoingTransferSize(self, *args):
        return _ezsp.EZSPInterface_emberSetMaximumOutgoingTransferSize(self, *args)



    def emberSetDescriptorCapability(self, *args):
        return _ezsp.EZSPInterface_emberSetDescriptorCapability(self, *args)



    def emberGetLastStackZigDevRequestSequence(self):
        return _ezsp.EZSPInterface_emberGetLastStackZigDevRequestSequence(self)



    def emberAesMmoHashInit(self, *args):
        return _ezsp.EZSPInterface_emberAesMmoHashInit(self, *args)



    def emberAesMmoHashUpdate(self, *args):
        return _ezsp.EZSPInterface_emberAesMmoHashUpdate(self, *args)



    def emberAesMmoHashFinal(self, *args):
        return _ezsp.EZSPInterface_emberAesMmoHashFinal(self, *args)



    def emberAesHashSimple(self, *args):
        return _ezsp.EZSPInterface_emberAesHashSimple(self, *args)



    def emberSendRemoveDevice(self, *args):
        return _ezsp.EZSPInterface_emberSendRemoveDevice(self, *args)



    def emberSendUnicastNetworkKeyUpdate(self, *args):
        return _ezsp.EZSPInterface_emberSendUnicastNetworkKeyUpdate(self, *args)



    def emberGetCurrentNetwork(self):
        return _ezsp.EZSPInterface_emberGetCurrentNetwork(self)



    def emberSetCurrentNetwork(self, *args):
        return _ezsp.EZSPInterface_emberSetCurrentNetwork(self, *args)



    def emberGetCallbackNetwork(self):
        return _ezsp.EZSPInterface_emberGetCallbackNetwork(self)



    def emberFindAndRejoinNetworkWithReason(self, *args):
        return _ezsp.EZSPInterface_emberFindAndRejoinNetworkWithReason(self, *args)



    def emberGetLastRejoinReason(self):
        return _ezsp.EZSPInterface_emberGetLastRejoinReason(self)



    def emberGetLastLeaveReason(self):
        return _ezsp.EZSPInterface_emberGetLastLeaveReason(self)



    def ezspStackStatusHandler(self):
        return _ezsp.EZSPInterface_ezspStackStatusHandler(self)



    def ezspIncomingMessageHandler(self, *args):
        return _ezsp.EZSPInterface_ezspIncomingMessageHandler(self, *args)



    def ezspMessageSentHandler(self, *args):
        return _ezsp.EZSPInterface_ezspMessageSentHandler(self, *args)



    def ezspEnergyScanResultHandler(self):
        return _ezsp.EZSPInterface_ezspEnergyScanResultHandler(self)



    def ezspScanCompleteHandler(self):
        return _ezsp.EZSPInterface_ezspScanCompleteHandler(self)



    def ezspNetworkFoundHandler(self, *args):
        return _ezsp.EZSPInterface_ezspNetworkFoundHandler(self, *args)



    def ezspChildJoinHandler(self):
        return _ezsp.EZSPInterface_ezspChildJoinHandler(self)



    def ezspIncomingSenderEui64Handler(self):
        return _ezsp.EZSPInterface_ezspIncomingSenderEui64Handler(self)



    def ezspTrustCenterJoinHandler(self):
        return _ezsp.EZSPInterface_ezspTrustCenterJoinHandler(self)



    def ezspTimerHandler(self):
        return _ezsp.EZSPInterface_ezspTimerHandler(self)



    def ezspRemoteSetBindingHandler(self, *args):
        return _ezsp.EZSPInterface_ezspRemoteSetBindingHandler(self, *args)



    def ezspRemoteDeleteBindingHandler(self):
        return _ezsp.EZSPInterface_ezspRemoteDeleteBindingHandler(self)



    def ezspPollCompleteHandler(self):
        return _ezsp.EZSPInterface_ezspPollCompleteHandler(self)



    def ezspPollHandler(self):
        return _ezsp.EZSPInterface_ezspPollHandler(self)



    def ezspIncomingRouteRecordHandler(self):
        return _ezsp.EZSPInterface_ezspIncomingRouteRecordHandler(self)



    def ezspIncomingManyToOneRouteRequestHandler(self):
        return _ezsp.EZSPInterface_ezspIncomingManyToOneRouteRequestHandler(self)



    def ezspIncomingRouteErrorHandler(self):
        return _ezsp.EZSPInterface_ezspIncomingRouteErrorHandler(self)



    def ezspIdConflictHandler(self):
        return _ezsp.EZSPInterface_ezspIdConflictHandler(self)



    def ezspMacPassthroughMessageHandler(self):
        return _ezsp.EZSPInterface_ezspMacPassthroughMessageHandler(self)



    def ezspMacFilterMatchMessageHandler(self):
        return _ezsp.EZSPInterface_ezspMacFilterMatchMessageHandler(self)



    def ezspRawTransmitCompleteHandler(self):
        return _ezsp.EZSPInterface_ezspRawTransmitCompleteHandler(self)



    def ezspSwitchNetworkKeyHandler(self):
        return _ezsp.EZSPInterface_ezspSwitchNetworkKeyHandler(self)



    def ezspZigbeeKeyEstablishmentHandler(self):
        return _ezsp.EZSPInterface_ezspZigbeeKeyEstablishmentHandler(self)



    def ezspGenerateCbkeKeysHandler(self, *args):
        return _ezsp.EZSPInterface_ezspGenerateCbkeKeysHandler(self, *args)



    def ezspCalculateSmacsHandler(self, *args):
        return _ezsp.EZSPInterface_ezspCalculateSmacsHandler(self, *args)



    def ezspDsaSignHandler(self):
        return _ezsp.EZSPInterface_ezspDsaSignHandler(self)



    def ezspDsaVerifyHandler(self):
        return _ezsp.EZSPInterface_ezspDsaVerifyHandler(self)



    def ezspMfglibRxHandler(self):
        return _ezsp.EZSPInterface_ezspMfglibRxHandler(self)



    def ezspIncomingBootloadMessageHandler(self):
        return _ezsp.EZSPInterface_ezspIncomingBootloadMessageHandler(self)



    def ezspBootloadTransmitCompleteHandler(self):
        return _ezsp.EZSPInterface_ezspBootloadTransmitCompleteHandler(self)



    def ezspInit(self):
        return _ezsp.EZSPInterface_ezspInit(self)



    def ezspClose(self):
        return _ezsp.EZSPInterface_ezspClose(self)



    def ezspCallbackPending(self):
        return _ezsp.EZSPInterface_ezspCallbackPending(self)



    def ezspWakeUp(self):
        return _ezsp.EZSPInterface_ezspWakeUp(self)


    __swig_setmethods__['ezspSleepMode'] = _ezsp.EZSPInterface_ezspSleepMode_set
    __swig_getmethods__['ezspSleepMode'] = _ezsp.EZSPInterface_ezspSleepMode_get
    if _newclass:
        ezspSleepMode = _swig_property(_ezsp.EZSPInterface_ezspSleepMode_get, _ezsp.EZSPInterface_ezspSleepMode_set)
    __swig_setmethods__['instanceCount'] = _ezsp.EZSPInterface_instanceCount_set
    __swig_getmethods__['instanceCount'] = _ezsp.EZSPInterface_instanceCount_get
    if _newclass:
        instanceCount = _swig_property(_ezsp.EZSPInterface_instanceCount_get, _ezsp.EZSPInterface_instanceCount_set)

    def callback_ezspStackStatusHandler(self, status):
        pass



    def callback_ezspIncomingMessageHandler(self, type, frame, lastHopLqi, lastHopRssi, sender, bindingIndex, addressIndex, message):
        pass



    def callback_ezspMessageSentHandler(self, type, indexOrDestination, apsFrame, messageTag, status, message):
        pass



    def callback_ezspEnergyScanResultHandler(self, channel, maxRssiValue):
        pass



    def callback_ezspScanCompleteHandler(self, channel, status):
        pass



    def callback_noCallback(self):
        pass



    def callback_ezspNetworkFoundHandler(self, network, lastHopLqi, lastHopRssi):
        pass



    def callback_ezspChildJoinHandler(self, index, joining, childID, childEui64, childType):
        pass



    def callback_ezspIncomingSenderEui64Handler(self, senderEui64):
        pass



    def callback_ezspTrustCenterJoinHandler(self, newNodeId, newNodeEui64, status, policyDecision, parentOfNewNodeId):
        pass



    def callback_ezspTimerHandler(self, timerId):
        pass



    def callback_ezspRemoteSetBindingHandler(self, entry, index, policyDecision):
        pass



    def callback_ezspRemoteDeleteBindingHandler(self, index, policyDecision):
        pass



    def callback_ezspPollCompleteHandler(self, status):
        pass



    def callback_ezspPollHandler(self, childId):
        pass



    def callback_ezspIncomingRouteRecordHandler(self, source, sourceEui, lastHopLqi, lastHopRssi, relayList):
        pass



    def callback_ezspIncomingManyToOneRouteRequestHandler(self, source, longId, cost):
        pass



    def callback_ezspIncomingRouteErrorHandler(self, status, target):
        pass



    def callback_ezspIdConflictHandler(self, id):
        pass



    def callback_ezspMacPassthroughMessageHandler(self, messageType, lastHopLqi, lastHopRssi, message):
        pass



    def callback_ezspMacFilterMatchMessageHandler(self, filterIndexMatch, legacyPassthroughType, lastHopLqi, lastHopRssi, message):
        pass



    def callback_ezspRawTransmitCompleteHandler(self, status):
        pass



    def callback_ezspSwitchNetworkKeyHandler(self, sequenceNumber):
        pass



    def callback_ezspZigbeeKeyEstablishmentHandler(self, partner, status):
        pass



    def callback_ezspCalculateSmacsHandler(self, status, initiatorSmac, responderSmac):
        pass



    def callback_ezspDsaSignHandler(self, status, message):
        pass



    def callback_ezspDsaVerifyHandler(self, status):
        pass



    def callback_ezspMfglibRxHandler(self, linkQuality, rssi, packet):
        pass



    def callback_ezspIncomingBootloadMessageHandler(self, longId, lastHopLqi, lastHopRssi, message):
        pass



    def callback_ezspBootloadTransmitCompleteHandler(self, status, message):
        pass



    def callback_unhandledCallback(self, callback):
        pass



    def dispatchCallback(self, callback):
        if callback == EZSP_NO_CALLBACKS:
            self.callback_noCallback()
        elif callback == EZSP_STACK_STATUS_HANDLER:
            self.callback_ezspStackStatusHandler(self.ezspStackStatusHandler())
        elif callback == EZSP_INCOMING_MESSAGE_HANDLER:
            frame = EmberApsFrame()
            (type, lastHopLqi, lastHopRssi, sender, bindingIndex, addressIndex, message,) = self.ezspIncomingMessageHandler(frame)
            self.callback_ezspIncomingMessageHandler(type, frame, lastHopLqi, lastHopRssi, sender, bindingIndex, addressIndex, message)
        elif callback == EZSP_MESSAGE_SENT_HANDLER:
            frame = EmberApsFrame()
            (type, indexOrDestination, messageTag, status, message,) = self.ezspMessageSentHandler(frame)
            self.callback_ezspMessageSentHandler(type, indexOrDestination, frame, messageTag, status, message)
        elif callback == EZSP_ENERGY_SCAN_RESULT_HANDLER:
            (channel, maxRssiValue,) = self.ezspEnergyScanResultHandler()
            self.callback_ezspEnergyScanResultHandler(channel, maxRssiValue)
        elif callback == EZSP_SCAN_COMPLETE_HANDLER:
            (channel, status,) = self.ezspScanCompleteHandler()
            self.callback_ezspScanCompleteHandler(channel, status)
        elif callback == EZSP_NETWORK_FOUND_HANDLER:
            network = EmberZigbeeNetwork()
            (lastHopLqi, lastHopRssi,) = self.ezspNetworkFoundHandler(network)
            self.callback_ezspNetworkFoundHandler(network, lastHopLqi, lastHopRssi)
        elif callback == EZSP_CHILD_JOIN_HANDLER:
            (index, joining, childID, childEui64, childType,) = self.ezspChildJoinHandler()
            self.callback_ezspChildJoinHandler(index, joining, childID, childEui64, childType)
        elif callback == EZSP_INCOMING_SENDER_EUI64_HANDLER:
            senderEui64 = self.ezspIncomingSenderEui64Handler()
            self.callback_ezspIncomingSenderEui64Handler(senderEui64)
        elif callback == EZSP_TRUST_CENTER_JOIN_HANDLER:
            (newNodeId, newNodeEui64, status, policyDecision, parentOfNewNodeId,) = self.ezspTrustCenterJoinHandler()
            self.callback_ezspTrustCenterJoinHandler(newNodeId, newNodeEui64, status, policyDecision, parentOfNewNodeId)
        elif callback == EZSP_TIMER_HANDLER:
            timerId = self.ezspTimerHandler()
            self.callback_ezspTimerHandler(timerId)
        elif callback == EZSP_REMOTE_SET_BINDING_HANDLER:
            entry = EmberBindingTableEntry()
            (index, policyDecision,) = self.ezspRemoteSetBindingHandler(entry)
            self.callback_ezspRemoteSetBindingHandler(entry, index, policyDecision)
        elif callback == EZSP_REMOTE_DELETE_BINDING_HANDLER:
            (index, policyDecision,) = self.ezspRemoteDeleteBindingHandler()
            self.callback_ezspRemoteDeleteBindingHandler(index, policyDecision)
        elif callback == EZSP_POLL_COMPLETE_HANDLER:
            status = self.ezspPollCompleteHandler()
            self.callback_ezspPollCompleteHandler(status)
        elif callback == EZSP_POLL_HANDLER:
            childId = self.ezspPollHandler()
            self.callback_ezspPollHandler(childId)
        elif callback == EZSP_INCOMING_ROUTE_RECORD_HANDLER:
            (source, sourceEui, lastHopLqi, lastHopRssi, relayList,) = self.ezspIncomingRouteRecordHandler()
            self.callback_ezspIncomingRouteRecordHandler(source, sourceEui, lastHopLqi, lastHopRssi, relayList)
        elif callback == EZSP_INCOMING_MANY_TO_ONE_ROUTE_REQUEST_HANDLER:
            (source, longId, cost,) = self.ezspIncomingManyToOneRouteRequestHandler()
            self.callback_ezspIncomingManyToOneRouteRequestHandler(source, longId, cost)
        elif callback == EZSP_INCOMING_ROUTE_ERROR_HANDLER:
            (status, target,) = self.ezspIncomingRouteErrorHandler()
            self.callback_ezspIncomingRouteErrorHandler(status, target)
        elif callback == EZSP_ID_CONFLICT_HANDLER:
            id = self.ezspIdConflictHandler()
            self.callback_ezspIdConflictHandler(id)
        elif callback == EZSP_MAC_PASSTHROUGH_MESSAGE_HANDLER:
            (messageType, lastHopLqi, lastHopRssi, message,) = self.ezspMacPassthroughMessageHandler()
            self.callback_ezspMacPassthroughMessageHandler(messageType, lastHopLqi, lastHopRssi, message)
        elif callback == EZSP_MAC_FILTER_MATCH_MESSAGE_HANDLER:
            (filterIndexMatch, legacyPassthroughType, lastHopLqi, lastHopRssi, message,) = ezspMacFilterMatchMessageHandler()
            self.callback_ezspMacFilterMatchMessageHandler(filterIndexMatch, legacyPassthroughType, lastHopLqi, lastHopRssi, message)
        elif callback == EZSP_RAW_TRANSMIT_COMPLETE_HANDLER:
            status = self.ezspRawTransmitCompleteHandler()
            self.callback_ezspRawTransmitCompleteHandler(status)
        elif callback == EZSP_SWITCH_NETWORK_KEY_HANDLER:
            sequenceNumber = self.ezspSwitchNetworkKeyHandler()
            self.callback_ezspSwitchNetworkKeyHandler(sequenceNumber)
        elif callback == EZSP_ZIGBEE_KEY_ESTABLISHMENT_HANDLER:
            (partner, status,) = self.ezspZigbeeKeyEstablishmentHandler()
            self.callback_ezspZigbeeKeyEstablishmentHandler(partner, status)
        elif callback == EZSP_GENERATE_CBKE_KEYS_HANDLER:
            ephemeralPublicKey = EmberPublicKeyData()
            status = self.ezspGenerateCbkeKeysHandler(ephemeralPublicKey)
            self.callback_ezspGenerateCbkeKeysHandler(status, ephemeralPublicKey)
        elif callback == EZSP_CALCULATE_SMACS_HANDLER:
            initiatorSmac = EmberSmacData()
            responderSmac = EmberSmacData()
            status = self.ezspCalculateSmacsHandler(initiatorSmac, responderSmac)
            self.callback_ezspCalculateSmacsHandler(status, initiatorSmac, responderSmac)
        elif callback == EZSP_DSA_SIGN_HANDLER:
            (status, message,) = self.ezspDsaSignHandler()
            self.callback_ezspDsaSignHandler(status, message)
        elif callback == EZSP_DSA_VERIFY_HANDLER:
            status = self.ezspDsaVerifyHandler()
            self.callback_ezspDsaVerifyHandler(status)
        elif callback == EZSP_MFGLIB_RX_HANDLER:
            (linkQuality, rssi, packet,) = self.ezspMfglibRxHandler()
            self.callback_ezspMfglibRxHandler(linkQuality, rssi, packet)
        elif callback == EZSP_INCOMING_BOOTLOAD_MESSAGE_HANDLER:
            (longId, lastHopLqi, lastHopRssi, message,) = self.ezspIncomingBootloadMessageHandler()
            self.callback_ezspIncomingBootloadMessageHandler(longId, lastHopLqi, lastHopRssi, message)
        elif callback == EZSP_BOOTLOAD_TRANSMIT_COMPLETE_HANDLER:
            (status, message,) = self.ezspBootloadTransmitCompleteHandler()
            self.callback_ezspBootloadTransmitCompleteHandler(status, message)
        else:
            self.callback_unhandledCallback(callback)



    def __init__(self):
        this = _ezsp.new_EZSPInterface()
        try:
            self.this.append(this)
        except:
            self.this = this


    __swig_destroy__ = _ezsp.delete_EZSPInterface
    __del__ = lambda self: None

EZSPInterface_swigregister = _ezsp.EZSPInterface_swigregister
EZSPInterface_swigregister(EZSPInterface)

+++ okay decompyling ./ezsp.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2016.01.27 00:42:44 MSK
