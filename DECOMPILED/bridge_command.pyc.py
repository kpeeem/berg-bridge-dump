# 2016.01.27 00:42:34 MSK
import time
import byte_tuple
import json

class BridgeCommand(object):

    def __init__(self, **kwargs):
        self.timestamp = time.time()
        self.bridge_address = kwargs.pop('bridge_address', None)
        self.command_name = kwargs.pop('command_name', None)
        self.command_id = kwargs.pop('command_id', None)
        self.params = kwargs.pop('params')
        self.completed = False
        self._return_code = None
        self.url = None



    @classmethod
    def from_json(cls, cloud_dictionary):
        init_params = {}
        init_params['bridge_address'] = cloud_dictionary['bridge_address']
        init_params['command_id'] = cloud_dictionary['command_id']
        json_payload = cloud_dictionary['json_payload']
        init_params['command_name'] = json_payload['name']
        init_params['params'] = json_payload['params']
        instance = cls(**init_params)
        return instance



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
        return 'BridgeCommand: timestamp %s, bridge_address: %s, command_name: %s, command_id: %s, params: %s' % (self.timestamp,
         self.bridge_address_hex,
         self.command_name,
         self.command_id,
         self.params)



    @property
    def return_code(self):
        return self._return_code



    @return_code.setter
    def return_code(self, value):
        if self.completed == False:
            self.completed = True
        self._return_code = value



    def to_json(self):
        if not self.completed:
            raise RuntimeError, 'to_json() called on non-completed command'
        json_hash = {'type': 'BridgeCommandResponse'}
        json_hash['timestamp'] = time.time()
        json_hash['bridge_address'] = self.bridge_address_hex
        json_hash['command_id'] = self.command_id
        json_hash['return_code'] = self.return_code
        return json.dumps(json_hash)



    def param_value_for_key(self, key):
        if self.params != None and self.params.has_key(key):
            return self.params[key]
        else:
            return 




+++ okay decompyling ./bridge_command.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2016.01.27 00:42:34 MSK
