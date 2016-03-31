# 2016.01.27 00:43:02 MSK
import os
os.environ['CUSTOM_CHIP_SELECT_DEVICE'] = '/sys/class/gpio/gpio71/value'
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/vendor')
import optparse
import api
import code
import threading
import thread
import base64
import struct
import Queue
import time
import signal
import logging
import struct
import random
import string
from socket import gethostname
from singleton import Singleton
import berg_cloud_socket_api
import cloud_log_record
import linux_hub
import status_server
import watchdog_monitor
import statistics_monitor
import customlogger
import version
import ezsp
import byte_tuple
import bridge_command
import device_command
PID_FILE = '/var/run/bergcloud_bridge.pid'
LOG_QUEUE_SIZE = 50
COMMAND_QUEUE_SIZE = 10
EVENT_QUEUE_SIZE = 10
MAX_SUCCESSIVE_UPSTREAM_ERRORS = 20

class BergCloudSocketBridge():

    def __init__(self, options, log_queue):
        self.options = options
        self.log_queue = log_queue
        self.event_queue = Queue.Queue(EVENT_QUEUE_SIZE)
        self.command_queue = Queue.Queue(COMMAND_QUEUE_SIZE)
        self.logger = customlogger.Logger('bridge')
        self.shutdown_triggered = False
        self.should_reboot = False
        self.should_restart = False



    def run(self):
        global app
        linux_hub.setup_gpio()
        linux_hub.reset_ncp()
        linux_hub.set_up_ipv4_timeouts()
        bridge_config = {'extended_pan_id_prefix': 1111839303L,
         'radio_power': 8,
         'network_create': True,
         'network_permit_joining': True,
         'print_progress_dots': False,
         'purge_link_keys': True}
        random.seed()
        bridge_config['extended_pan_id'] = (bridge_config['extended_pan_id_prefix'] << 32) + random.getrandbits(32)
        try:
            self.device = api.WeminucheApi(self.event_queue, bridge_config)
        except:
            self.logger.critical('Failed to initialise the NCP')
            self.shutdown(14)
            return 
        self.device.energyScanRequest(0)
        while not app.device.channelScanResultsReady():
            time.sleep(0.1)

        (total, failed, energies,) = app.device.collectAndClearChannelScanResults()
        lowest_energy = 0
        selected_channel = 0
        for energy in energies:
            (channel, dbm,) = energy
            if dbm < lowest_energy:
                selected_channel = channel
                lowest_energy = dbm

        self.logger.info('Switching to channel %d with lowest energy %d' % (selected_channel, lowest_energy))
        app.device.channelChangeRequest(selected_channel)
        self.system_environment = self.collectEnvironment()
        self.host_eui64 = self.device.getHostEui64()
        self.host_eui64_hex = byte_tuple.eui64ToHexString(self.host_eui64, False)
        self.watchdog_thread_exit_event = threading.Event()
        self.watchdog_delegate = watchdog_monitor.WatchdogMonitor(self.options.watchdog, self.watchdog_thread_exit_event)
        self.watchdog_thread = threading.Thread(target=self.watchdog_delegate.patWatchdog)
        self.watchdog_thread.start()
        self.device.setTelemetryDelegate(statistics_monitor.StatisticsMonitor(self))
        self.berg_cloud_thread_exit_event = threading.Event()
        self.berg_cloud_api = berg_cloud_socket_api.BergCloudSocketApi(self, self.host_eui64_hex, self.berg_cloud_thread_exit_event, self.command_queue, self.event_queue, self.log_queue, self.watchdog_delegate)
        self.berg_cloud_thread = threading.Thread(target=self.berg_cloud_api.start)
        self.berg_cloud_thread.start()
        self.ver_info = version.Version()
        self.ver_info.ncp_stack_version = self.device.getStackVersionString()
        self.logger.info('Starting webserver')
        self.httpd = status_server.BottleStats()
        self.httpd.set_bridge(self)
        self.webserver_thread = threading.Thread(target=self.httpd.run)
        self.webserver_thread.start()
        self.device.setWatchdogDelegate(self.watchdog_delegate)
        self.command_thread_exit_event = threading.Event()
        self.command_thread = threading.Thread(target=self.runQueuedCommands)
        self.command_thread.start()
        self.zigbee_led_thread_exit_event = threading.Event()
        self.zigbee_led_thread = threading.Thread(target=self.checkConnectedDevices)
        self.zigbee_led_thread.start()
        if self.options.daemon:
            while self.shutdown_triggered == False:
                try:
                    time.sleep(1)
                except KeyboardInterrupt:
                    self.logger.critical('Shutdown triggered in app.run() with KeyboardInterrupt')
                    self.shutdown()




    def collectEnvironment(self):
        system_env = {}
        system_env['network_info'] = self.device.getNetworkInformationDict()
        environment_dump = ''
        try:
            with open('/tmp/uboot.env') as f:
                environment_dump = f.read()
        except IOError as e:
            environment_dump = os.popen('/usr/sbin/fw_printenv').read()
        if len(environment_dump) > 0:
            encoded_environment_dump = base64.standard_b64encode(environment_dump)
            system_env['uboot_environment'] = encoded_environment_dump
        try:
            with open('/proc/uptime') as f:
                system_env['uptime'] = f.read().rstrip()
        except:
            pass
        ip_address = linux_hub.get_ip('eth0')
        system_env['local_ip_address'] = ip_address
        return system_env



    def shutdown(self, signum = None, frame = None):
        if self.shutdownInProgress():
            return 
        self.shutdown_triggered = True
        if signum:
            self.logger.critical('Shutdown triggered with signal %d' % signum)
            shutdown_called_directly = False
        else:
            self.logger.critical('Shutdown called directly')
            shutdown_called_directly = True
        self.stopThreads(shutdown_called_directly)
        self.removePIDFile()
        linux_hub.set_led_state('zigbee', 'off')
        linux_hub.set_led_state('bergcloud', 'off')
        linux_hub.hold_reset_ncp()
        self.logger.critical('Shutdown complete!')
        sys.stderr = sys.__stderr__
        sys.stdout = sys.__stdout__
        sys.stdout.flush()
        sys.stderr.flush()
        if not self.options.daemon:
            self.logger.critical('Shutdown complete. Please exit the interactive prompt if you have one open')
        elif self.should_reboot == True:
            self.logger.critical('Farewell! (99)')
            sys.exit(99)
        if signum == 14:
            self.logger.critical('Goodbye! (1)')
            sys.exit(1)
        else:
            self.logger.critical('See you soon! (0)')
            sys.exit(0)



    def shutdownInProgress(self):
        if self.shutdown_triggered:
            self.logger.warning('Shutdown already in progress')
            return True
        else:
            return False



    def stopThreads(self, shutdown_called_directly = False):
        self.logger.critical('Shutting down threads...')
        if hasattr(self, 'webserver_thread'):
            while self.webserver_thread.isAlive():
                self.httpd.stop()

            self.logger.critical('Debug webserver thread finished')
        if hasattr(self, 'berg_cloud_thread'):
            if self.berg_cloud_thread.isAlive():
                self.berg_cloud_thread_exit_event.set()
                self.berg_cloud_thread.join()
            if not self.berg_cloud_thread.isAlive():
                self.logger.critical('Socket thread finished')
        if hasattr(self, 'device'):
            self.device.shutdown()
            self.logger.critical('Zigbee device thread finished')
        if hasattr(self, 'command_thread') and self.command_thread.isAlive():
            self.command_thread_exit_event.set()
            if not shutdown_called_directly:
                self.command_thread.join()
                self.logger.critical('Command thread finished')
        if hasattr(self, 'zigbee_led_thread') and self.zigbee_led_thread.isAlive():
            self.zigbee_led_thread_exit_event.set()
            self.zigbee_led_thread.join()
            self.logger.critical('LED control finished')
        if hasattr(self, 'watchdog_thread') and self.watchdog_thread.isAlive():
            self.watchdog_thread_exit_event.set()
            self.watchdog_thread.join()
            self.logger.critical('Watchdog thread finished')



    def removePIDFile(self):
        if os.path.exists(PID_FILE):
            os.unlink(PID_FILE)
            self.logger.info('Removed PID file')



    def runQueuedCommands(self):
        self.logger.debug('Starting command thread')
        event_state = self.command_thread_exit_event.wait(0.1)
        while not event_state:
            if self.watchdog_delegate:
                self.watchdog_delegate.updateKey('commandThread')
            try:
                command = self.command_queue.get(False)
                self.executeCommand(command)
            except Queue.Empty:
                pass
            if self.berg_cloud_api.connection_failure_count > MAX_SUCCESSIVE_UPSTREAM_ERRORS:
                self.should_reboot = True
                self.logger.warning('should_reboot is now true')
            if self.should_restart == True or self.should_reboot == True:
                time.sleep(1)
                if self.options.daemon:
                    self.logger.warning('Interrupting the main thread with SIGINT')
                    os.kill(os.getpid(), signal.SIGINT)
                else:
                    self.logger.warning('Calling shutdown')
                    self.shutdown()
            event_state = self.command_thread_exit_event.wait(0.1)




    def executeCommand(self, command):
        sm = statistics_monitor.StatisticsMonitor()
        if isinstance(command, bridge_command.BridgeCommand):
            self.logger.debug("Executing bridge command '%s'" % command.command_name)
            try:
                command.return_code = self.executeBridgeCommand(command)
            except:
                self.logger.exception('Unexpected command thread error:', sys.exc_info())
                command.return_code = 255
        elif isinstance(command, device_command.DeviceCommand):
            self.logger.debug('Delivering command payload to device %s' % command.device_address_hex)
            try:
                command.return_code = self.executeDeviceCommand(command)
                command.transfer_time = sm.commandTransferTime()
                command.rssi_stats = sm.rssiStatsForEui64(command.device_address_hex)
                sm.commandComplete(command.return_code)
            except:
                self.logger.exception('Unexpected log queue thread error:', sys.exc_info())
                command.return_code = 255
        self.logger.debug('Enqueueing completed command into event queue')
        self.event_queue.put(command, True)



    def executeDeviceCommand(self, command):
        start_time = time.time()
        payload_length = command.payload_length
        status = self.device.executeCommand(command)
        end_time = time.time()
        elapsed_time = end_time - start_time
        bytes_per_second = payload_length / elapsed_time
        self.logger.info('Completed transfer in %f seconds (%.0f B/s, %0.2f kB/s)' % (elapsed_time, bytes_per_second, bytes_per_second / 1024.0))
        return status



    def executeBridgeCommand(self, command):
        start_time = time.time()
        command_name = command.command_name
        self.logger.debug('Running executeBridgeCommand with %s' % command)
        if command.command_name == 'add_device_encryption_key':
            if command.params.has_key('device_address') and command.params.has_key('encryption_key'):
                device_address = command.params['device_address']
                encryption_key_base64 = command.params['encryption_key']
                encryption_key_bin = base64.b64decode(encryption_key_base64)
                encryption_key_seq = struct.unpack('BBBBBBBBBBBBBBBB', encryption_key_bin)
                self.device.TCAddOrUpdateKey(byte_tuple.convertToEui64(device_address), encryption_key_seq)
                return 0
            raise TypeError, "BridgeCommand 'add_device_encryption_key' takes two arguments, 'device_address' and 'encryption_key'"
        elif command.command_name == 'set_cloud_log_level':
            lm = customlogger.LoggerManager()
            level = command.param_value_for_key('level')
            if isinstance(level, int):
                level = command.params['level']
                if level < 10:
                    level = 10
                elif level > 50:
                    level = 50
            if isinstance(level, str) or isinstance(level, unicode):
                level = level.lower()
                log_level = logging.WARNING
                if level == 'debug':
                    log_level = logging.DEBUG
                elif level == 'info':
                    log_level = logging.INFO
                elif level == 'warning':
                    log_level = logging.WARNING
                elif level == 'error':
                    log_level = logging.ERROR
                elif level == 'critical':
                    log_level = logging.CRITICAL
                self.logger.debug('Setting cloud logging level to %d' % log_level)
                result = lm.setCloudLoggingLevel(log_level)
                return result
            raise TypeError, "BridgeCommand 'set_cloud_log_level' takes a 'level' argument of type string"
        elif command.command_name == 'leave':
            result = self.device.emberLeaveNetwork()
            return result
        if command.command_name == 'form':
            channels = command.param_value_for_key('channels')
            if not isinstance(channels, list):
                channels = [11,
                 14,
                 15,
                 19,
                 20,
                 24,
                 25]
            result = self.device.scanForUnusedPanId(channels)
            return result
        if command.command_name == 'pjoin':
            duration = command.param_value_for_key('duration')
            if isinstance(duration, str) or isinstance(duration, int) or isinstance(duration, unicode):
                self.device.emberPermitJoining(int(duration))
            else:
                self.device.emberPermitJoining(255)
        else:
            if command.command_name == 'restart':
                self.logger.warning("Issuing 'restart' flag!")
                self.should_restart = True
                return 0
            else:
                if command.command_name == 'reboot':
                    self.logger.warning("Issuing 'reboot' flag!")
                    self.should_reboot = True
                    return 0
                self.logger.error("Unknown BridgeCommand name '%s'" % command.command_name)
                return 1



    def networkUp(self):
        return self.device.emberNetworkState() == ezsp.EMBER_JOINED_NETWORK



    def checkConnectedDevices(self):
        while not self.zigbee_led_thread_exit_event.isSet():
            if self.watchdog_delegate:
                self.watchdog_delegate.updateKey('ledThread')
            if self.networkUp() == False:
                linux_hub.set_led_state('zigbee', 'off', True)
                self.zigbee_led_thread_exit_event.wait(1)
            elif self.event_queue.full():
                linux_hub.zigbee_event_queue_full_sequence(self.zigbee_led_thread_exit_event)
                self.zigbee_led_thread_exit_event.wait(1)
            elif len(self.berg_cloud_api.event_sources.keys()) == 0:
                linux_hub.zigbee_searching_sequence(self.zigbee_led_thread_exit_event)
            else:
                linux_hub.set_led_state('zigbee', 'on', True)
                self.zigbee_led_thread_exit_event.wait(1)




    def leave(self):
        command = bridge_command.BridgeCommand()
        command.command_name = 'leave'
        self.executeBridgeCommand(command)



    def form(self, channels = None):
        default_channels = [11,
         14,
         15,
         19,
         20,
         24,
         25]
        if channels == None:
            channels = default_channels
        command = bridge_command.BridgeCommand()
        command.command_name = 'form'
        command.params = {'channels': channels}
        self.executeBridgeCommand(command)



    def setcll(self, mode = None):
        if mode == None:
            print 'setcll requires an argument to set the logging level'
            print '  setcll(logging.DEBUG) for everything'
            print '  setcll(logging.INFO) for info and above'
            print '  setcll(logging.WARNING) for warning and above'
            print '  setcll(logging.ERROR) for errors and above'
            print '  setcll(logging.CRITICAL) for critical messages only'
        else:
            lm = customlogger.LoggerManager()
            lm.setCloudLoggingLevel(mode)



    def setfll(self, mode = None):
        if mode == None:
            print 'setfll requires an argument to set the file logging level'
            print '  setfll(logging.DEBUG) for everything'
            print '  setfll(logging.INFO) for info and above'
            print '  setfll(logging.WARNING) for warning and above'
            print '  setfll(logging.ERROR) for errors and above'
            print '  setfll(logging.CRITICAL) for critical messages only'
        else:
            lm = customlogger.LoggerManager()
            lm.setFileLoggingLevel(mode)



    def zinfo(self):
        self.logger.info('----- Network info ------')
        nwk_info = self.device.getNetworkInformation()
        [ self.logger.info('%s' % line.strip()) for line in nwk_info ]
        self.logger.info('----- Route table ------')
        route_info = self.device.getRouteTableInformationArray()
        [ self.logger.info('%s' % line.strip()) for line in route_info ]
        self.logger.info('----- Child table ------')
        children = self.device.getChildTableInformationArray()
        [ self.logger.info('%s' % line) for line in children ]
        self.logger.info('------ Address table ------')
        address_table = self.device.getAddressTableInformationArray()
        [ self.logger.info('%s' % line) for line in address_table ]



    def cinfo(self):
        print 'Socket info:'
        print ''
        print 'Socket state: %s' % self.berg_cloud_api.ws.connectionState
        if self.berg_cloud_api.last_connected_at != None:
            print 'Connected at: %s' % time.strftime('%a, %d %b %Y %H:%M:%S', time.gmtime(self.berg_cloud_api.last_connected_at))
            print 'Connected to: %s' % berg_cloud_socket_api.STREAMING_URI



    def chaninfo(self):
        self.logger.info('  Total transmissions = %i' % self.cachedTotalProbeTransmissions)
        self.logger.info('  Transmission failures = %i' % self.cachedFailedProbeTransmissions)
        self.logger.info('  Channel energies:')
        for chaninfo in self.cachedChannelEnergies:
            self.logger.info('    %02i : %02i dBm' % (chaninfo[0], chaninfo[1]))




    def help(self):
        print 'Available commands:'
        print '  app.form()         - Form the Zigbee network'
        print '  app.leave()        - Unform the Zigbee network'
        print '  app.setcll(level)  - Set the cloud log level. Valid values are:'
        print '                       logging.DEBUG, logging.INFO, logging.WARNING,'
        print '                       logging.ERROR, logging.CRITICAL'
        print '  app.setfll(level)  - Set the file log level. Valid values are as above'
        print '  app.zinfo()        - Print Zigbee network info'
        print '  app.cinfo()        - Print BERG Cloud socket connection info'



if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('--pid', action='store_true', dest='pid', default=False, help='write a PID file to %s' % PID_FILE)
    parser.add_option('--daemon', action='store_true', dest='daemon', default=False, help='Run in daemon mode with no interactive prompt')
    parser.add_option('--logfile', action='store_true', dest='logfile', default=False, help='Also log output to a file')
    parser.add_option('--logfile-level', action='store', type='string', dest='logfile_level', default='', help='Default log level for logfile')
    parser.add_option('--cloudlog', action='store_true', dest='cloudlog', default=False, help='Also log output to the cloud')
    parser.add_option('--cloudlog-level', action='store', dest='cloudlog_level', default='', help='Sets the verbosity of cloud logging')
    parser.add_option('--webdebug', action='store_true', dest='webdebug', default=False, help='Enable the internal debug webserver')
    parser.add_option('--htmllog', action='store_true', dest='htmllog', default=False, help='Also log output to the internal status webpage')
    parser.add_option('--watchdog', action='store_true', dest='watchdog', default=False, help='Enable Linux kernel watchdog usage')
    (options, args,) = parser.parse_args()
    if options.pid:
        if os.path.exists(PID_FILE):
            with open(PID_FILE, 'r') as f:
                running_pid = f.read()
            raise Exception('Script is already running with pid %s. Remove %s if the process is no longer running' % (running_pid, PID_FILE))
        else:
            pid = str(os.getpid())
            with open(PID_FILE, 'w') as f:
                f.write(pid)
    log_queue = None
    if options.cloudlog or options.htmllog:
        log_queue = Queue.Queue(LOG_QUEUE_SIZE)
    customlogger.LoggerManager(options.daemon, options.logfile, log_queue)
    app = BergCloudSocketBridge(options, log_queue)
    if options.logfile_level != '':
        app.setfll(int(options.logfile_level))
    if options.cloudlog_level != '':
        app.setcll(int(options.cloudlog_level))
    if options.daemon:
        sys.stdout = customlogger.StdOutLogger()
        sys.stderr = customlogger.StdErrLogger()
        signal.signal(signal.SIGTERM, app.shutdown)
        signal.signal(signal.SIGINT, app.shutdown)
        signal.signal(signal.SIGALRM, app.shutdown)
        print 'Loggers and signal handlers installed',
    app.run()
    if not options.daemon:
        help = 'Type app.help() for more detailed help'
        sys.ps1 = '%s >>> ' % gethostname()
        code.interact(local=locals(), banner='Bridge console: (app.help() for info)')
        app.shutdown()

+++ okay decompyling ./weminuche_bridge.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2016.01.27 00:43:05 MSK
