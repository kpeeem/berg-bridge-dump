# 2016.01.27 00:42:49 MSK
import struct
import os
import socket
import hashlib
import time
import fcntl
import customlogger
import pynetlinux
EVENT_KEY = 1
EMBER_NWAKE = 56
EMBER_NRST = 70
EMBER_NSSEL = 71
LED_ZIGBEE = 86
LED_BERG_CLOUD = 87
LED_ETHERNET = 88

def quick_write(path, value):
    with open(path, 'w') as f:
        f.write(value)



def quick_read(path):
    with open(path, 'r') as f:
        value = f.read().strip()
    return value



def setup_gpio():
    logger = customlogger.Logger('gpio')
    gpio_ports = [EMBER_NWAKE,
     EMBER_NRST,
     EMBER_NSSEL,
     LED_BERG_CLOUD,
     LED_ZIGBEE]
    for port in gpio_ports:
        logger.debug("Setting GPIO port %d to 'out'" % port)
        gpio_export(port, 'out')




def gpio_export(number, direction, value = 1):
    path_prefix = '/sys/class/gpio/'
    export_path = path_prefix + 'export'
    direction_path = path_prefix + 'gpio%d/direction' % number
    value_path = path_prefix + 'gpio%d/value' % number
    if not os.path.exists(value_path):
        print 'GPIO export of %d' % number
        quick_write(export_path, str(number))
    existing_direction = quick_read(direction_path)
    if existing_direction != direction:
        print "GPIO direction doesn't match: %s != %s" % (existing_direction, direction)
        quick_write(direction_path, direction)
    quick_write(value_path, str(value))



def gpio_set_value(number, value):
    path_prefix = '/sys/class/gpio/'
    value_path = path_prefix + 'gpio%d/value' % number
    quick_write(value_path, str(value))



def blocking_read_from_event(filter_event_number, filter_event_code):
    input_event_format = 'iihhi'
    input_event_size = 16
    ev_path = '/dev/input/event%d' % filter_event_number
    ev_fd = open(ev_path, 'rb')
    try:
        event = ev_fd.read(input_event_size)
        while event:
            (ev_time1, ev_time2, ev_type, ev_code, ev_value,) = struct.unpack(input_event_format, event)
            if ev_type == EVENT_KEY and ev_code == filter_event_code:
                return (ev_time1 + ev_time2 / 1000000.0, ev_value)
            event = ev_fd.read(input_event_size)

    finally:
        ev_fd.close()



def reset_ncp():
    logger = customlogger.Logger('gpio')
    logger.debug('Resetting NCP')
    gpio_set_value(EMBER_NRST, 0)
    time.sleep(1)
    gpio_set_value(EMBER_NRST, 1)
    time.sleep(1)



def hold_reset_ncp():
    gpio_set_value(EMBER_NRST, 0)



def set_led_state(name, state = 'off', quiet = False):
    logger = customlogger.Logger('gpio')
    if state == 'on':
        value = 0
    else:
        value = 1
    if name == 'bergcloud':
        gpio_set_value(LED_BERG_CLOUD, value)
    elif name == 'zigbee':
        gpio_set_value(LED_ZIGBEE, value)
    elif name == 'ethernet':
        gpio_set_value(LED_ETHERNET, value)
    else:
        logger.warning("Unknown LED '%s'" % name)
        return 
    if not quiet:
        logger.info("Setting LED '%s' to '%s'" % (name, state))



def test_eth0_link_up():
    path = '/sys/class/net/eth0/carrier'
    try:
        fd = open(path, 'r')
        state = fd.read()
        fd.close()
        if state == '1\n':
            return True
        else:
            return False
    except:
        return False



def get_ip(iface = 'eth0'):
    SIOCGIFADDR = 35093
    ifreq = struct.pack('16sH14s', iface, socket.AF_INET, '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    result = make_ioctl(ifreq, SIOCGIFADDR)
    if result:
        ip = struct.unpack('16sH2x4s8x', result)[2]
        return socket.inet_ntoa(ip)



def get_mac(iface = 'eth0'):
    SIOCGIFHWADDR = 35111
    ifreq = struct.pack('16sH14s', iface, socket.AF_INET, '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    result = make_ioctl(ifreq, SIOCGIFHWADDR)
    if result:
        return ''.join([ '%02x:' % ord(char) for char in result[18:24] ])[:-1]



def make_ioctl(ifreq, ioctl):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockfd = sock.fileno()
    try:
        res = fcntl.ioctl(sockfd, ioctl, ifreq)
        return res
    except:
        return None



def zigbee_searching_sequence(event):
    set_led_state('zigbee', 'on', True)
    event.wait(0.087)
    set_led_state('zigbee', 'off', True)
    event.wait(0.11)
    set_led_state('zigbee', 'on', True)
    event.wait(0.087)
    set_led_state('zigbee', 'off', True)
    event.wait(1.35)



def zigbee_event_queue_full_sequence(event):
    set_led_state('zigbee', 'on', True)
    event.wait(0.2)
    set_led_state('zigbee', 'off', True)
    event.wait(0.087)
    set_led_state('zigbee', 'on', True)
    event.wait(0.2)
    set_led_state('zigbee', 'off', True)
    event.wait(0.087)
    set_led_state('zigbee', 'on', True)
    event.wait(0.2)
    set_led_state('zigbee', 'off', True)
    event.wait(0.087)
    set_led_state('zigbee', 'on', True)
    event.wait(0.2)
    set_led_state('zigbee', 'off', True)



def get_eth_speed():
    ifs = pynetlinux.ifconfig.list_ifs()
    if len(ifs) == 0:
        return (None, None, None, None)
    eth = ifs[0]
    return eth.get_link_info()



def set_eth_speed(speed):
    ifs = pynetlinux.ifconfig.list_ifs()
    if len(ifs) == 0:
        return (None, None, None, None)
    eth = ifs[0]
    eth.set_link_mode(speed, True)



def set_up_ipv4_timeouts():
    base_path = '/proc/sys/net/ipv4/'
    quick_write(base_path + 'tcp_keepalive_time', '5')
    quick_write(base_path + 'tcp_keepalive_intvl', '1')
    quick_write(base_path + 'tcp_keepalive_probes', '5')
    quick_write(base_path + 'tcp_retries2', '3')



+++ okay decompyling ./linux_hub.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2016.01.27 00:42:50 MSK
