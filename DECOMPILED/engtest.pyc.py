# 2016.01.27 00:42:38 MSK
import customlogger
import linux_hub
import api
import Queue
import socket
import fcntl
import struct
import sys
import time

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 35093, struct.pack('256s', ifname[:15]))[20:24])


if __name__ == '__main__':
    customlogger.LoggerManager(True)
    zigbee_functional = False
    tcpip_functional = False
    linux_hub.setup_gpio()
    linux_hub.reset_ncp()
    dummy_queue = Queue.Queue(1)
    bridge_config = {'extended_pan_id': 0,
     'radio_power': 8,
     'network_create': False,
     'network_permit_joining': False,
     'print_progress_dots': False,
     'purge_link_keys': True}
    try:
        device = api.WeminucheApi(dummy_queue, bridge_config)
        device.getStackVersionString()
        device.shutdown()
        zigbee_functional = True
        print 'Zigbee functional'
    except:
        print 'Zigbee non-functional'
    try:
        ip = get_ip_address('eth0')
        print 'Ethernet/IP functional'
        tcpip_functional = True
    except:
        print 'Ethernet/IP non-functional'
    flip_flop = 'off'
    while True:
        if flip_flop == 'on':
            flip_flop = 'off'
        else:
            flip_flop = 'on'
        if zigbee_functional:
            linux_hub.set_led_state('zigbee', flip_flop)
        if tcpip_functional:
            linux_hub.set_led_state('ethernet', flip_flop)
            linux_hub.set_led_state('bergcloud', flip_flop)
        time.sleep(0.01)

    print 'Finished engineering test procedure'
    sys.exit(0)

+++ okay decompyling ./engtest.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2016.01.27 00:42:39 MSK
