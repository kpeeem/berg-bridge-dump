# 2016.01.27 00:42:37 MSK
import time
import byte_tuple
import device_command
RSP_SUCCESS = 0
RSP_EUI64_NOT_FOUND = 1
RSP_FAILED_NETWORK = 2
RSP_INVALID_SEQUENCE = 32
RSP_INVALID_SIZE = 128
RSP_INVALID_DEVICETYPE = 129
RSP_FILESYSTEM_ERROR = 130

class DeviceCommandResponse(object):
    responseDict = {RSP_SUCCESS: 'RSP_SUCCESS',
     RSP_EUI64_NOT_FOUND: 'RSP_EUI64_NOT_FOUND',
     RSP_FAILED_NETWORK: 'RSP_FAILED_NETWORK',
     RSP_INVALID_SEQUENCE: 'RSP_INVALID_SEQUENCE',
     RSP_INVALID_SIZE: 'RSP_INVALID_SIZE',
     RSP_INVALID_DEVICETYPE: 'RSP_INVALID_DEVICETYPE',
     RSP_FILESYSTEM_ERROR: 'RSP_FILESYSTEM_ERROR'}

    def __init__(self, **kwargs):
        self.timestamp = time.time()
        self.return_code = None
        self.device_address = kwargs.pop('device_address', None)
        self.response_url = kwargs.pop('response_url', None)



    @classmethod
    def from_device_command(cls, device_command):
        init_params = {}
        init_params['response_url'] = device_command.url + '/response'
        init_params['device_address'] = device_command.device_address
        instance = cls(**init_params)
        return instance



    @property
    def device_address(self):
        return self._device_address



    @device_address.setter
    def device_address(self, value):
        if isinstance(value, tuple) or value == None:
            self._device_address = value
        else:
            self._device_address = byte_tuple.convertToEui64(value)



    def device_address_hex(self):
        return byte_tuple.tupleToHexString(self._device_address, 16)



    def __repr__(self):
        if self.responseDict.has_key(self.return_code):
            return 'DeviceCommandResponse URL %s returning %s' % (self.response_url, self.responseDict[self.return_code])
        else:
            return 'DeviceCommandResponse URL %s returning %d' % (self.response_url, self.return_code)




+++ okay decompyling ./device_command_response.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2016.01.27 00:42:38 MSK
