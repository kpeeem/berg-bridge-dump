# 2016.01.27 00:42:32 MSK
import time
from singleton import Singleton
from ws4py.client.threadedclient import WebSocketClient
import ssl
import sys
import Queue
import errno
import random
import bridge_command
import bridge_event
import device_command
import device_event
import cloud_log_record
import linux_hub
import simple_caching_resolver
import statistics_monitor
from urlparse import urlparse
from customlogger import Logger
from singleton import Singleton
import version
import byte_tuple
import socket
import json
import os
HTTP_SOCKET_TIMEOUT = 30
THREAD_WAIT_TIMEOUT = 0.1
HEARTBEAT_TIMEOUT = 30
custom_url = os.environ.get('CUSTOM_ENDPOINT', None)
if custom_url:
    u = urlparse(custom_url)
    WS_SCHEME = u.scheme
    WS_HOSTNAME = u.hostname
    WS_PORT = str(u.port)
else:
    WS_SCHEME = 'https'
    WS_HOSTNAME = 'bridge.bergcloud.com'
    WS_PORT = '443'
SSL_KEY = '/etc/ssl/private/bridge-main-client.key'
SSL_CERT = '/etc/ssl/certs/bridge-main-client.crt'
SSL_CA_PEM = '/etc/ssl/ca/cacert.pem'

class BergCloudSocketApi(Singleton):

    def __init__(self, bridge, host_eui64_hex, thread_exit_event, command_queue, event_queue, log_queue, watchdog_delegate):
        self.host_eui64_hex = host_eui64_hex
        self.commandProcessingEnabled = True
        self.eventProcessingEnabled = True
        self.logProcessingEnabled = True
        self.thread_exit_event = thread_exit_event
        self.command_queue = command_queue
        self.event_queue = event_queue
        self.log_queue = log_queue
        self.watchdog_delegate = watchdog_delegate
        self.current_json_message = None
        self.bridge = bridge
        self.networkUp = bridge.networkUp
        self.handshake_sent = False
        self.logger = Logger('cloud')
        self.command_logger = Logger('cloud.command')
        self.event_logger = Logger('cloud.event')
        self.logging_logger = Logger('cloud.logging')
        self.socket_logger = Logger('cloud.socket')
        self.resolver = simple_caching_resolver.SimpleCachingResolver()
        self.sm = statistics_monitor.StatisticsMonitor()
        self.event_sources = {}
        self.connection_failure_count = 0
        self.ip_pool = []
        self.last_connected_at = None
        self.ws = None
        socket.setdefaulttimeout(HTTP_SOCKET_TIMEOUT)



    def start(self):
        event_state = self.thread_exit_event.wait(THREAD_WAIT_TIMEOUT)
        while not event_state:
            if self.watchdog_delegate:
                self.watchdog_delegate.updateKey('socketThread')
            try:
                if self.ws == None or self.ws.connectionState == 'closed':
                    if len(self.ip_pool) == 0:
                        (ip_addresses, expiration_time,) = self.resolver.lookup(WS_HOSTNAME)
                        random.shuffle(ip_addresses)
                        self.logger.info('IP pool now %s with an expiry in %d seconds' % (ip_addresses, expiration_time - time.time()))
                        self.ip_pool = ip_addresses
                        self.connection_expiration_time = expiration_time
                    ip_address = self.ip_pool.pop()
                    if self.connect(ip_address):
                        self.last_connected_at = time.time()
                        self.current_ip_address = ip_address
                        self.socket_logger.debug('Resetting connection_failure_count')
                        self.connection_failure_count = 0
                        self.handshake_sent = False
                    elif len(self.ip_pool) == 0:
                        self.connection_failure_count += 1
                        self.socket_logger.debug("Incrementing connection_failure_count (now %d) as we're out of IPs" % self.connection_failure_count)
                    event_state = self.thread_exit_event.wait(5)
                elif time.time() > self.connection_expiration_time:
                    if self.currentIPIsValid():
                        self.logger.info('DNS timeout reached: Current IP address is still valid, not dropping')
                        self.connection_expiration_time += 3600
                    else:
                        self.logger.info("Closing websocket as we're over expiry time and DNS has changed")
                        self.ws.close()
                else:
                    self.sendPendingData()
            except:
                self.socket_logger.exception('Unhandled socket api exception:', sys.exc_info())
                self.connection_failure_count += 1
                self.handshake_sent = False
            event_state = self.thread_exit_event.wait(THREAD_WAIT_TIMEOUT)

        if self.ws != None:
            self.logger.warning('Closing websocket from bridge side')
            try:
                self.ws.close()
            finally:
                if self.ws._th.isAlive():
                    self.ws._th.join()
                self.ws = None



    def currentIPIsValid(self):
        current_ip_address = self.current_ip_address
        (resolved_ip_addresses, expiration_time,) = self.resolver.lookup(WS_HOSTNAME)
        return current_ip_address in resolved_ip_addresses



    def sendPendingData(self):
        if self.current_json_message != None:
            self.socket_logger.info('We have pending JSON data to send: %s' % self.current_json_message)
            if self.sendJson(self.current_json_message):
                self.current_json_message = None
            else:
                self.socket_logger.warning("Still can't send the current JSON")
                return 
        if not self.handshake_sent:
            self.onEstablishConnection()
        if self.eventProcessingEnabled:
            self.postFromEventQueue()
        if self.log_queue != None and self.logProcessingEnabled:
            self.postFromLogQueue()
        self.assess_active_devices()



    def endpoint(self):
        return '%s://%s:%s/' % (WS_SCHEME, WS_HOSTNAME, WS_PORT)



    def connect(self, ip_address):
        connect_success = False
        self.socket_logger.info('Creating websocket client')
        ssl_options = None
        ws_protocols = ['bergcloud-bridge-v1']
        if WS_SCHEME == 'https':
            proto = 'wss'
            ssl_options = {'keyfile': SSL_KEY,
             'certfile': SSL_CERT,
             'ca_certs': SSL_CA_PEM,
             'cert_reqs': ssl.CERT_REQUIRED}
        else:
            proto = 'ws'
        ws_uri = '%s://%s:%s/api/v1/connection' % (proto, ip_address, WS_PORT)
        try:
            if ssl_options == None:
                self.ws = BergCloudStreamingClient(ws_uri, protocols=ws_protocols, heartbeat_freq=5)
            else:
                self.ws = BergCloudStreamingClient(ws_uri, ssl_options=ssl_options, protocols=ws_protocols, heartbeat_freq=5)
            self.ws.daemon = False
            self.ws.set_command_queue(self.command_queue)
            self.ws.set_event_queue(self.event_queue)
            self.ws.set_host_eui64_hex(self.host_eui64_hex)
            self.socket_logger.debug('Connecting to %s' % ws_uri)
            self.ws.connect()
            connect_success = True
        except socket.error as e:
            if e.errno == errno.ECONNREFUSED:
                self.socket_logger.error('Socket connection refused')
            elif e.errno == errno.ETIMEDOUT:
                self.socket_logger.error('Socket connection timed out')
            elif e.errno == errno.EHOSTUNREACH:
                self.socket_logger.error('No route to host')
            else:
                self.socket_logger.error('Socket connection exception %s [%s]' % (e, str(e.errno)))
        except socket.timeout:
            self.socket_logger.error('Socket connection timed out')
        except:
            self.socket_logger.exception('Unexpected socket connect error:', sys.exc_info())
        if not connect_success:
            self.ws = None
        return connect_success



    def isConnected(self):
        if self.ws == None:
            return False
        else:
            return self.ws.connectionState == 'connected'



    def onEstablishConnection(self):
        if self.networkUp():
            self.socket_logger.info('Sending bridge power_on handshake')
            event = bridge_event.BridgeEvent(self.host_eui64_hex, {'name': 'power_on'})
            event.append_payload(self.bridge.system_environment)
            ver_info = version.Version()
            version_dict = {'firmware_version': ver_info.firmware_version,
             'mac_address': ver_info.mac_address,
             'ncp_version': ver_info.ncp_stack_version,
             'model': ver_info.model}
            event.append_payload(version_dict)
            event_json = event.to_json()
            self.logger.debug('Posting event JSON %s' % event_json)
            result = self.sendJson(event_json)
            if result:
                self.handshake_sent = True
                self.event_sources = {}



    def postFromEventQueue(self):
        try:
            event = self.event_queue.get(False)
            if isinstance(event, device_event.DeviceEvent) and event.device_address == None:
                self.logger.warning('Device Event has no device_address! Cannot post to cloud!')
                return 
            if isinstance(event, device_event.DeviceEvent):
                source_eui64_hex = byte_tuple.eui64ToHexString(event.device_address, False)
                self._register_active_device(source_eui64_hex)
                event.rssi_stats = self.sm.rssiStatsForEui64(source_eui64_hex)
            self.current_json_message = event.to_json()
            self.logger.info('Posting event JSON %s' % self.current_json_message)
            result = self.sendJson(self.current_json_message)
            if result:
                self.current_json_message = None
        except Queue.Empty:
            pass



    def postFromLogQueue(self):
        log_records = []
        try:
            while True:
                record = self.log_queue.get(False)
                clr = cloud_log_record.CloudLogRecord(record)
                log_records.append(clr)

        except Queue.Empty:
            if len(log_records) > 0:
                self.current_json_message = cloud_log_record.CloudLogRecord.to_json(log_records, self.host_eui64_hex)
                result = self.sendJson(self.current_json_message)
                if result:
                    self.current_json_message = None



    def sendJson(self, json):
        if self.ws == None:
            self.logger.error('No socket client to post with!')
            return False
        try:
            self.ws.send(json)
            return True
        except socket.error as e:
            if e.errno == errno.EPIPE:
                self.logger.error('Broken pipe. Re-stashing event and reconnecting')
                time.sleep(2)
            else:
                self.logger.error('Socket error %s' % e)
            self.ws.close()
            self.ws = None
            return False
        except:
            self.logger.exception('socket send exception', sys.exc_info())
            return False



    def assess_active_devices(self):
        current_time = time.time()
        nodes = []
        for eui64_hex in self.event_sources.keys():
            times = self.event_sources[eui64_hex]
            first_contact_time = times[0]
            last_contact_time = times[1]
            if current_time - last_contact_time < HEARTBEAT_TIMEOUT:
                nodes.append(eui64_hex)
            else:
                self._deregister_active_device(eui64_hex)

        if len(nodes) == 0:
            return None
        else:
            return nodes



    def active_device_uptime(self, eui64_hex):
        current_time = time.time()
        if self.event_sources.has_key(eui64_hex):
            return current_time - self.event_sources[eui64_hex][0]



    def _register_active_device(self, eui64_hex):
        current_time = time.time()
        if self.event_sources.has_key(eui64_hex):
            self.event_sources[eui64_hex][1] = current_time
        else:
            self.event_sources[eui64_hex] = [current_time, current_time]
            self.command_logger.info('Issuing device_connect for %s' % eui64_hex)
            event = bridge_event.BridgeEvent(self.host_eui64_hex, {'name': 'device_connect',
             'device_address': eui64_hex})
            self.event_queue.put(event, False)



    def _deregister_active_device(self, eui64_hex):
        if self.event_sources.has_key(eui64_hex):
            self.command_logger.info('Issuing device_disconnect for %s' % eui64_hex)
            event = bridge_event.BridgeEvent(self.host_eui64_hex, {'name': 'device_disconnect',
             'device_address': eui64_hex})
            self.event_queue.put(event, False)
            del self.event_sources[eui64_hex]




class BergCloudStreamingClient(WebSocketClient):

    def __init__(self, *args, **kwargs):
        self.logger = Logger('cloud.socketclient')
        self.connectionState = 'connecting'
        super(BergCloudStreamingClient, self).__init__(*args, **kwargs)



    def set_command_queue(self, queue):
        self.command_queue = queue



    def set_event_queue(self, queue):
        self.event_queue = queue



    def set_host_eui64_hex(self, value):
        self.host_eui64_hex = value



    def opened(self):
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 3)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 3)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 5)
        self.connectionState = 'connected'
        linux_hub.set_led_state('bergcloud', 'on', True)
        self.logger.info('Websocket open and connected')



    def closed(self, code, reason = None):
        self.connectionState = 'closed'
        linux_hub.set_led_state('bergcloud', 'off', True)
        self.logger.warning('Closed down websocket, code: %d, reason: %s' % (code, reason))



    def received_message(self, m):
        try:
            decoded_json_message = json.loads(str(m))
            self.process_command(decoded_json_message)
        except:
            self.logger.exception('Exception decoding JSON:', sys.exc_info())



    def process_command(self, response):
        if response.has_key('type'):
            command_type = response['type']
            if command_type == 'BridgeCommand':
                bc = bridge_command.BridgeCommand.from_json(response)
                self.logger.debug('Queueing %s' % bc)
                self.command_queue.put(bc, False)
            elif command_type == 'DeviceCommand':
                try:
                    dc = device_command.DeviceCommand.from_json(response)
                    dc.bridge_address = self.host_eui64_hex
                    self.logger.debug('Queueing %s' % dc)
                    self.command_queue.put(dc, False)
                except Queue.Full:
                    self.logger.warning('Ut oh, the command queue is full!')
                    dc.return_code = device_command.RSP_QUEUE_FULL
                    self.event_queue.put(dc, False)
                except:
                    self.logger.exception('Exception creating command:', sys.exc_info())
                    dc.return_code = 255
                    self.event_queue.put(dc, False)
            else:
                self.logger.error("Unknown command type '%s'" % command_type)
                return 
        else:
            self.logger.error('Required type key missing in command')
            return 




+++ okay decompyling ./berg_cloud_socket_api.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2016.01.27 00:42:34 MSK
