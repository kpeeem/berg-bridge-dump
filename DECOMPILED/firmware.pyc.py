# 2016.01.27 00:42:44 MSK
PRINT_PROGRESS_DOTS = True
POLL_DELAY_S = 0.05
MAX_POLL_ATTEMPTS = 20
STANDALONE_BOOTLOADER_NORMAL_MODE = 1
STANDALONE_BOOTLOADER_RECOVERY_MODE = 0
XMODEM_BLOCK_SIZE = 128
XMODEM_SOH = 1
XMODEM_EOT = 4
XMODEM_ACK = 6
XMODEM_NAK = 21
XMODEM_CANCEL = 24
XMODEM_READY = 67
XMODEM_QUERY = 81
XMODEM_QRESP = 82
QRESP_OFFSET_BL_ACTIVE = 1
QRESP_OFFSET_MFG_ID = 2
QRESP_OFFSET_HARDWARE_TAG = 4
QRESP_OFFSET_BL_CAPS = 20
QRESP_OFFSET_PLATFORM = 21
QRESP_OFFSET_MICRO = 22
QRESP_OFFSET_PHY = 23
QRESP_OFFSET_BL_VERSION = 24
BOOTLOAD_PROTOCOL_VERSION = 1
import sys
import struct
import ezsp
import crc16pure as crc16
import time

def xmodemTransaction(i, message):
    i.bootSendMessage(message)
    completed = False
    attempts = MAX_POLL_ATTEMPTS
    while not completed:
        if attempts == 0:
            raise RuntimeError('Timed out waiting for XMODEM ACK')
        attempts -= 1
        queryResponse = i.XModemPollForResult(False)
        if queryResponse != None:
            if queryResponse[0] == XMODEM_ACK:
                completed = True
            else:
                raise RuntimeError('Unexpected XMODEM response (0x%02x)' % queryResponse[0])
        if not completed:
            time.sleep(POLL_DELAY_S)




def updateNCP(firmwareEBL):
    with open(firmwareEBL, 'rb') as file:
        i = ezsp.EZSPInterface()
        i.ezspInit()
        queryResponse = i.XModemQuery(False)
        if not queryResponse:
            i.ezspVersion(4)
            i.ezspLaunchStandaloneBootloader(STANDALONE_BOOTLOADER_RECOVERY_MODE)
            i.waitFor260boot()
            queryResponse = i.XModemQuery(False)
            if not queryResponse:
                raise RuntimeError('Cannot start NCP bootloader')
        if queryResponse[0] != XMODEM_QRESP:
            raise RuntimeError('Invalid response from NCP bootloader')
        if queryResponse[QRESP_OFFSET_PLATFORM] != 4:
            raise RuntimeError('Invalid bootloader "platform" value')
        if queryResponse[QRESP_OFFSET_MICRO] != 3:
            raise RuntimeError('Invalid bootloader "micro" value')
        bootloaderVersion = queryResponse[QRESP_OFFSET_BL_VERSION] << 8 | queryResponse[(QRESP_OFFSET_BL_VERSION + 1)]
        print 'NCP bootloader version: 0x%04x' % bootloaderVersion
        blockCount = 1
        pktCounter = 0
        complete = False
        while not complete:
            packet = file.read(XMODEM_BLOCK_SIZE)
            if len(packet) < XMODEM_BLOCK_SIZE:
                complete = True
            if len(packet) > 0:
                while len(packet) < XMODEM_BLOCK_SIZE:
                    packet += chr(255)

                xmodemPacket = struct.pack('>BBBB128sH', BOOTLOAD_PROTOCOL_VERSION, XMODEM_SOH, blockCount, 255 - blockCount, packet, crc16.crc16xmodem(packet))
                xmodemTransaction(i, xmodemPacket)
                pktCounter += 1
                blockCount += 1
                if blockCount > 255:
                    blockCount = 0
            if PRINT_PROGRESS_DOTS:
                print '.',

        xmodemPacket = struct.pack('>BB', BOOTLOAD_PROTOCOL_VERSION, XMODEM_EOT)
        xmodemTransaction(i, xmodemPacket)


if __name__ == '__main__':
    updateNCP(sys.argv[1])

+++ okay decompyling ./firmware.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2016.01.27 00:42:44 MSK
