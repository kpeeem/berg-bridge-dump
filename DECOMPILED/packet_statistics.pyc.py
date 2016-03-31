# 2016.01.27 00:42:52 MSK
import time

class PacketStatistics:

    def __init__(self, nodeId, lqi, rssi):
        self.timestamp = time.time()
        self.nodeId = nodeId
        self.lqi = lqi
        self.rssi = rssi



    def __repr__(self):
        return 'Node ID = 0x%04x, LQI = %i/255, RSSI = %i dBm' % (self.nodeId, self.lqi, self.rssi)



    def to_list(self):
        return ('0x%04x' % self.nodeId,
         time.strftime('%a %H:%M:%S', time.gmtime(self.timestamp)),
         self.lqi,
         self.rssi)




+++ okay decompyling ./packet_statistics.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2016.01.27 00:42:52 MSK
