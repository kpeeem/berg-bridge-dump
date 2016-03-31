# 2016.01.27 00:42:54 MSK
from singleton import Singleton
import time
import device_command_response
import customlogger
import byte_tuple

class StatisticsMonitor(Singleton):

    def init(self, app = None):
        if app != None:
            self.app = app
        self.logger = customlogger.Logger('StatisticsMonitor')
        self.destination_eui64 = None
        self.commandLoopedTransfer = False
        self.loopNumber = 0
        self.successfulCommandTransfers = 0
        self.commandTransferring = False
        self.commandDestinationEui64 = None
        self.commandStartTime = 0
        self.commandEndTime = 0
        self.lastCommandSuccessful = False
        self.commandBytesTransferred = 0
        self.packetFailedCount = 0
        self.htmlLogLines = []
        self.loggedPacketsStatistics = {}
        self.packetLimit = 20



    def deviceDeregistered(self, device):
        pass



    def deviceRegistered(self, device):
        pass



    def commandTransferStarted(self, device_address, command_size):
        self.commandDestinationEui64 = device_address
        if not self.commandLoopedTransfer:
            self.packetFailedCount = 0
        self.commandTransferring = True
        self.commandStartTime = time.time()
        self.commandBytesTransferred = 0



    def commandTransferEnded(self, success):
        self.commandTransferring = False
        self.lastCommandSuccessful = success
        self.commandEndTime = time.time()



    def packetFailed(self, count = 1):
        self.packetFailedCount += count



    def incrementCommandBytesTransferred(self, size):
        self.commandBytesTransferred += size



    def commandTransferSpeed(self):
        if self.commandTransferring:
            startTime = self.commandStartTime
            if self.commandTransferring:
                endTime = time.time()
            else:
                endTime = self.commandEndTime
            speed = self.commandBytesTransferred / (endTime - startTime)
        else:
            speed = 0
        return speed



    def commandComplete(self, status):
        if self.commandLoopedTransfer:
            self.loopNumber += 1
            if status == device_command_response.RSP_SUCCESS:
                self.successfulCommandTransfers += 1



    def commandTransferTime(self):
        return round(self.commandEndTime - self.commandStartTime, 2)



    def packetsReceived(self, eui64, packetStatsList):
        if eui64 != None:
            eui64Hex = byte_tuple.eui64ToHexString(eui64, False)
            if self.loggedPacketsStatistics.has_key(eui64Hex):
                self.loggedPacketsStatistics[eui64Hex] += packetStatsList
            else:
                self.loggedPacketsStatistics[eui64Hex] = packetStatsList
            overflow = len(self.loggedPacketsStatistics[eui64Hex]) - self.packetLimit
            if overflow > 0:
                del self.loggedPacketsStatistics[eui64Hex][0:overflow]



    def rssiStatsForEui64(self, eui64Hex):
        if self.loggedPacketsStatistics.has_key(eui64Hex):
            counter = 0
            total_rssi = 0
            min_rssi = None
            max_rssi = None
            for stat in self.loggedPacketsStatistics[eui64Hex]:
                total_rssi += stat.rssi
                if min_rssi == None:
                    min_rssi = stat.rssi
                else:
                    min_rssi = min(min_rssi, stat.rssi)
                if max_rssi == None:
                    max_rssi = stat.rssi
                else:
                    max_rssi = max(max_rssi, stat.rssi)
                counter = counter + 1

            return [total_rssi / counter, min_rssi, max_rssi]
        else:
            return 




+++ okay decompyling ./statistics_monitor.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2016.01.27 00:42:56 MSK
