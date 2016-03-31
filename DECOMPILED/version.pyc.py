# 2016.01.27 00:43:01 MSK
from singleton import Singleton
import linux_hub

class Version(Singleton):
    BRIDGE_HARDWARE_MODEL = 'B'
    BRIDGE_MAJOR_VERSION = 2
    BRIDGE_MINOR_VERSION = 3
    BRIDGE_MAINT_VERSION = 1
    BRIDGE_BUILD_VERSION = 'f3c7946'
    BRIDGE_CLOUD_PROTOCOL_VERSION = 1

    def init(self):
        self._ncp_stack_version = 'Unknown'
        self._mac_address = linux_hub.get_mac('eth0')
        self._firmware_version = self.version_string



    @property
    def ncp_stack_version(self):
        return self._ncp_stack_version



    @ncp_stack_version.setter
    def ncp_stack_version(self, value):
        self._ncp_stack_version = value.rstrip('\n')



    @property
    def mac_address(self):
        return self._mac_address



    @property
    def firmware_version(self):
        return self._firmware_version



    @property
    def model(self):
        return Version.BRIDGE_HARDWARE_MODEL



    @property
    def long_version_string(self):
        s = 'BERG Cloud Bridge %s %s, MAC %s, NCP ver %s' % (Version.BRIDGE_HARDWARE_MODEL,
         self.version_string,
         self.mac_address,
         self.ncp_stack_version)
        return s



    @property
    def version_string(self):
        s = 'v%d.%d.%d-%s' % (Version.BRIDGE_MAJOR_VERSION,
         Version.BRIDGE_MINOR_VERSION,
         Version.BRIDGE_MAINT_VERSION,
         Version.BRIDGE_BUILD_VERSION)
        return s




+++ okay decompyling ./version.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2016.01.27 00:43:02 MSK
