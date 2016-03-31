# 2016.01.27 00:42:34 MSK
import time
import byte_tuple
import bridge_command

class BridgeCommandResponse(object):

    def __init__(self, **kwargs):
        self.timestamp = time.time()
        self.return_code = None
        self.response_url = kwargs.pop('response_url', None)



    @classmethod
    def from_bridge_command(cls, bridge_command):
        init_params = {}
        init_params['response_url'] = bridge_command.url + '/response'
        instance = cls(**init_params)
        return instance



    @property
    def bridge_address(self):
        return self.bridge_address



    @bridge_address.setter
    def bridge_address(self, value):
        if isinstance(value, tuple) or value == None:
            self.bridge_address = value
        else:
            byte_tuple.convertToEui64(value)



    def bridge_address_hex(self):
        return byte_tuple.tupleToHexString(self.bridge_address, 16)



    def __repr__(self):
        return 'BridgeCommandResponse URL %s returning %s' % (self.response_url, self.return_code)




+++ okay decompyling ./bridge_command_response.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2016.01.27 00:42:34 MSK
