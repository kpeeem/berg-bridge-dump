# 2016.01.27 00:42:35 MSK
import time
import json
import byte_tuple

class BridgeEvent(object):

    def __init__(self, bridge_address, payload = {}):
        self.timestamp = time.time()
        self.bridge_address = bridge_address
        self.payload = payload



    def __repr__(self):
        return 'BridgeEvent from bridge_address %s with payload %s' % (self.bridge_address_hex, self.payload)



    def append_payload(self, additional_dict):
        self.payload = dict(self.payload.items() + additional_dict.items())



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



    def to_hash(self):
        return {'type': 'BridgeEvent',
         'bridge_address': self.bridge_address_hex,
         'json_payload': self.payload,
         'timestamp': self.timestamp}



    def to_json(self):
        return json.dumps(self.to_hash())




+++ okay decompyling ./bridge_event.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2016.01.27 00:42:35 MSK
