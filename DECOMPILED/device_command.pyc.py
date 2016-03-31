# 2016.01.27 00:42:37 MSK
import time
import os
import StringIO
import byte_tuple
import json
import base64
RSP_SUCCESS = 0
RSP_EUI64_NOT_FOUND = 1
RSP_FAILED_NETWORK = 2
RSP_INVALID_SEQUENCE = 32
RSP_INVALID_SIZE = 128
RSP_INVALID_DEVICETYPE = 129
RSP_FILESYSTEM_ERROR = 130
RSP_QUEUE_FULL = 224

class DeviceCommand(object):
    RESPONSE_DICT = {RSP_SUCCESS: 'RSP_SUCCESS',
     RSP_EUI64_NOT_FOUND: 'RSP_EUI64_NOT_FOUND',
     RSP_FAILED_NETWORK: 'RSP_FAILED_NETWORK',
     RSP_INVALID_SEQUENCE: 'RSP_INVALID_SEQUENCE',
     RSP_INVALID_SIZE: 'RSP_INVALID_SIZE',
     RSP_INVALID_DEVICETYPE: 'RSP_INVALID_DEVICETYPE',
     RSP_FILESYSTEM_ERROR: 'RSP_FILESYSTEM_ERROR'}

    def __init__(self, **kwargs):
        self.timestamp = time.time()
        self.device_address = kwargs.pop('device_address', None)
        self.bridge_address = kwargs.pop('bridge_address', None)
        self.command_id = kwargs.pop('command_id', None)
        self.payload = kwargs.pop('payload', None)
        self.completed = False
        self._return_code = None
        self._rssi_stats = []
        self._transfer_time = 0
        self.url = None



    @classmethod
    def from_json(cls, cloud_dictionary):
        init_params = {}
        init_params['device_address'] = cloud_dictionary['device_address']
        init_params['payload'] = base64.b64decode(cloud_dictionary['binary_payload'])
        init_params['command_id'] = cloud_dictionary['command_id']
        instance = cls(**init_params)
        return instance



    @property
    def payload(self):
        return StringIO.StringIO(self._payload)



    @payload.setter
    def payload(self, value):
        self._payload = value



    @property
    def payload_length(self):
        return len(self._payload)



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



    def __repr__(self):
        return 'DeviceCommand: timestamp %s, device_address: %s, command_id: %s, payload_length: %d, completed: %d, return_code: %s' % (self.timestamp,
         self.device_address_hex,
         self.command_id,
         self.payload_length,
         self.completed,
         self.return_code_string)



    @property
    def return_code(self):
        return self._return_code



    @return_code.setter
    def return_code(self, value):
        if self.completed == False:
            self.completed = True
        self._return_code = value



    @property
    def rssi_stats(self):
        return self._rssi_stats



    @rssi_stats.setter
    def rssi_stats(self, value):
        self._rssi_stats = value



    @property
    def transfer_time(self):
        return self._transfer_time



    @transfer_time.setter
    def transfer_time(self, value):
        self._transfer_time = value



    @property
    def return_code_string(self):
        if self.return_code != None:
            return RESPONSE_DICT[self.return_code]
        else:
            return 



    def to_json(self):
        if not self.completed:
            raise RuntimeError, 'to_json() called on non-completed command'
        json_hash = {'type': 'DeviceCommandResponse'}
        json_hash['timestamp'] = time.time()
        json_hash['device_address'] = self.device_address_hex
        json_hash['bridge_address'] = self.bridge_address_hex
        json_hash['command_id'] = self.command_id
        json_hash['return_code'] = self.return_code
        json_hash['rssi_stats'] = self.rssi_stats
        json_hash['transfer_time'] = self.transfer_time
        return json.dumps(json_hash)




+++ okay decompyling ./device_command.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2016.01.27 00:42:37 MSK
