# 2016.01.27 00:42:38 MSK
import time
import base64
import struct
import byte_tuple
import json
import BERGCloudConst

class DeviceEvent(object):
    EVENT_HEADER_SIZE = 10
    EVENT_HEARTBEAT = 1
    EVENT_DID_PRINT = 2
    EVENT_DID_POWER_ON = 3
    EVENT_HEARTBEAT_SIZE = 4
    EVENT_DID_PRINT_SIZE = 5
    EVENT_DID_POWER_ON_SIZE_LONG = 74
    EVENT_DID_POWER_ON_SIZE_SHORT = 58
    resetDict = {0: 'Undeterminable cause',
     256: 'FIB bootloader',
     512: 'Ember bootloader',
     768: 'External reset',
     1024: 'Power on',
     1280: 'Watchdog',
     1536: 'Software triggered',
     1792: 'Software crash',
     2048: 'Flash failure',
     2304: 'Fatal error',
     2560: 'Access fault'}

    def __init__(self, bridge_address, device_address, payload):
        self.timestamp = time.time()
        self.bridge_address = bridge_address
        self.device_address = device_address
        self.payload = base64.b64encode(payload)
        self._rssi_stats = []



    def __repr__(self):
        return 'DeviceEvent from device_address %s of Base64 length %d' % (self.device_address_hex, len(self.payload))



    @property
    def device_address(self):
        return self._device_address



    @device_address.setter
    def device_address(self, value):
        if isinstance(value, tuple) or value == None:
            self._device_address = value
        else:
            self._device_address = byte_tuple.convertToEui64(value)



    @property
    def device_address_hex(self):
        return byte_tuple.eui64ToHexString(self.device_address, False)



    @property
    def bridge_address(self):
        return self._bridge_address



    @bridge_address.setter
    def bridge_address(self, value):
        if isinstance(value, tuple) or value == None:
            self._bridge_address = value
        else:
            self._bridge_address = byte_tuple.convertToEui64(value)



    @property
    def bridge_address_hex(self):
        if self.bridge_address != None:
            return byte_tuple.eui64ToHexString(self.bridge_address, False)
        else:
            return 



    @property
    def rssi_stats(self):
        return self._rssi_stats



    @rssi_stats.setter
    def rssi_stats(self, value):
        self._rssi_stats = value



    def to_hash(self):
        return {'type': 'DeviceEvent',
         'bridge_address': self.bridge_address_hex,
         'device_address': self.device_address_hex,
         'binary_payload': self.payload,
         'timestamp': time.time(),
         'rssi_stats': self.rssi_stats}



    def to_json(self):
        return json.dumps(self.to_hash())



    def to_unpacked_hash(self):
        pass




+++ okay decompyling ./device_event.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2016.01.27 00:42:38 MSK
