# 2016.01.27 00:42:50 MSK
import struct
import ezsp
import zdo

class NetworkManager:

    def setNetworkManagerRequest(self, networkManagerNodeId, activeChannels = ezsp.EMBER_ALL_802_15_4_CHANNELS_MASK):
        self.emberEnergyScanRequest(ezsp.EMBER_SLEEPY_BROADCAST_ADDRESS, activeChannels, 255, networkManagerNodeId)



    def energyScanRequest(self, nodeId, scanChannels = ezsp.EMBER_ALL_802_15_4_CHANNELS_MASK, scanDuration = 0, scanCount = 1):
        self.emberEnergyScanRequest(nodeId, scanChannels, scanDuration, scanCount)



    def channelChangeRequest(self, channel, nodeId = ezsp.EMBER_SLEEPY_BROADCAST_ADDRESS):
        self.emberEnergyScanRequest(nodeId, 1 << channel, 254, 0)



    def _nmProcessIncoming(self, sender, apsFrame, message):
        if apsFrame.clusterId == zdo.NWK_UPDATE_REQUEST:
            return True
        if apsFrame.clusterId == zdo.NWK_UPDATE_RESPONSE:
            (sequence, status,) = struct.unpack_from('<BB', message, 0)
            if status == zdo.EMBER_ZDP_SUCCESS:
                (scannedChannels, totalTransmissions, transmissionFailures, scannedChannelsListCount,) = struct.unpack_from('<LHHB', message, 2)
                channel = 0
                offset = 0
                channelEnergyList = []
                while channel < 32:
                    if scannedChannels & 1 << channel:
                        (channelEnergy,) = struct.unpack_from('<b', message, 11 + offset)
                        channelEnergyList.append((channel, channelEnergy))
                        offset += 1
                    channel += 1

                return self.callback_afNetworkUpdateResponseReceived(sender, totalTransmissions, transmissionFailures, channelEnergyList)
            self.logger.debug('Received ZDO message with status = 0x%02x' % status)
        return False



    def callback_afNetworkUpdateResponseReceived(self, sender, totalTransmissions, transmissionFailures, channelEnergyList):
        self.cachedChannelEnergies = []
        self.cachedTotalProbeTransmissions = totalTransmissions
        self.cachedFailedProbeTransmissions = transmissionFailures
        self.logger.info('Mgmt_NWK_Update_notify from node ID 0x%04x:' % sender)
        self.logger.info('  Total transmissions = %i' % totalTransmissions)
        self.logger.info('  Transmission failures = %i' % transmissionFailures)
        self.logger.info('  Channel energies:')
        for channelEnergy in channelEnergyList:
            self.cachedChannelEnergies.append((channelEnergy[0], channelEnergy[1]))
            self.logger.info('    %02i : %02i dBm' % (channelEnergy[0], channelEnergy[1]))

        self.channelScanResultsAvailable = True
        return True



    def channelScanResultsReady(self):
        if hasattr(self, 'channelScanResultsAvailable'):
            return True
        else:
            return False



    def collectAndClearChannelScanResults(self):
        result = (self.cachedTotalProbeTransmissions, self.cachedFailedProbeTransmissions, self.cachedChannelEnergies)
        del self.cachedChannelEnergies
        del self.cachedTotalProbeTransmissions
        del self.cachedFailedProbeTransmissions
        del self.channelScanResultsAvailable
        return result




+++ okay decompyling ./network_manager.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2016.01.27 00:42:51 MSK
