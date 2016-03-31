# 2016.01.27 00:42:57 MSK
import time
import BaseHTTPServer
import os
import socket
from singleton import Singleton
import customlogger
from os import sep
import device_command_response
import byte_tuple
import weminuche_bridge
import version
import linux_hub
import watchdog_monitor
import statistics_monitor
from urlparse import urlparse
import bottle

class InterruptableWSGIRefServer(bottle.ServerAdapter):
    server = None

    def run(self, handler):
        from wsgiref.simple_server import make_server, WSGIRequestHandler
        if self.quiet:

            class QuietHandler(WSGIRequestHandler):

                def log_request(*args, **kw):
                    pass



            self.options['handler_class'] = QuietHandler
        self.server = make_server(self.host, self.port, handler, **self.options)
        self.server.serve_forever()



    def stop(self):
        self.server.server_close()




class BottleStats(object):

    def store_custom_url(self, new_url):
        os.system('/bin/mount -o remount,rw /')
        PATH = '/usr/local/bergcloud-bridge/endpoint.override'
        try:
            with open(PATH, 'w') as f:
                f.write('export CUSTOM_ENDPOINT=%s' % new_url)
            success = True
        except:
            success = False
        os.system('/bin/mount -o remount,ro /')
        self._bridge.should_restart = True



    def set_bridge(self, bridge):
        self._bridge = bridge
        self._wdm = watchdog_monitor.WatchdogMonitor()
        self._sm = statistics_monitor.StatisticsMonitor()
        self._ver = version.Version()
        self._htmlLogLines = []



    def _auth(self, userpass):
        if userpass[0] == 'berg' and userpass[1] == 'hereandthere':
            return True
        else:
            return False



    def _route(self):
        self._app.route('/', method='GET', callback=self._redirect)
        self._app.route('/configure', method='GET', callback=self._endpoint)
        self._app.route('/configure', method='POST', callback=self._endpoint_post)
        self._app.route('/magic_debug', method='GET', callback=self._index)
        self._app.route('/css/<filename>', callback=self._static_asset)
        self._app.route('/js/<filename>', callback=self._static_asset)



    def _redirect(self):
        bottle.redirect('/configure')



    def _endpoint(self):
        auth = bottle.request.auth
        if not auth or not self._auth(auth):
            raise bottle.HTTPError(401, body='Unauthorized', header={'WWW-Authenticate': 'Basic realm="Log-in required"'})
        tpl_vars = {}
        tpl_vars['endpoint'] = self._bridge.berg_cloud_api.endpoint()
        tpl_vars['system_version'] = self._ver.version_string
        tpl_vars['system_ember_firmware'] = self._ver.firmware_version
        tpl_vars['system_mac_address'] = self._ver.mac_address
        tpl_vars['system_ncp_version'] = self._ver.ncp_stack_version
        if self._bridge.berg_cloud_api.isConnected():
            tpl_vars['connection_state_label_class'] = 'label-success'
            tpl_vars['connection_state'] = 'connected'
        else:
            tpl_vars['connection_state_label_class'] = 'label-warning'
            tpl_vars['connection_state'] = 'disconnected'
        tpl_out = bottle.template('/usr/local/bergcloud-bridge/webassets/endpoint.tpl', **tpl_vars)
        return tpl_out



    def _endpoint_post(self):
        auth = bottle.request.auth
        if not auth or not self._auth(auth):
            raise bottle.HTTPError(401, body='Unauthorized', header={'WWW-Authenticate': 'Basic realm="Log-in required"'})
        tpl_vars = {}
        tpl_vars['endpoint'] = self._bridge.berg_cloud_api.endpoint()
        tpl_vars['system_version'] = self._ver.version_string
        tpl_vars['system_ember_firmware'] = self._ver.firmware_version
        tpl_vars['system_mac_address'] = self._ver.mac_address
        tpl_vars['system_ncp_version'] = self._ver.ncp_stack_version
        if self._bridge.berg_cloud_api.isConnected():
            tpl_vars['connection_state_label_class'] = 'label-success'
            tpl_vars['connection_state'] = 'connected'
        else:
            tpl_vars['connection_state_label_class'] = 'label-warning'
            tpl_vars['connection_state'] = 'disconnected'
        ep = bottle.request.POST.get('endpoint', '').strip()
        u = urlparse(ep)
        error = None
        if u.scheme != 'https' and u.scheme != 'http':
            error = "You must specify either 'http' or 'https' in your URL"
        elif u.hostname == None:
            error = 'You must specify a hostname in your URL'
        elif u.port == None and u.scheme == 'https':
            port = 443
        elif u.port == None and u.scheme == 'http':
            port = 80
        else:
            port = u.port
        if error:
            tpl_vars['error'] = error
            tpl_vars['endpoint'] = ep
            return bottle.template('/usr/local/bergcloud-bridge/webassets/endpoint.tpl', **tpl_vars)
        else:
            final_url = '%s://%s:%d/' % (u.scheme, u.hostname, port)
            self.store_custom_url(final_url)
            tpl_vars['endpoint'] = final_url
            return bottle.template('/usr/local/bergcloud-bridge/webassets/endpoint_restart.tpl', **tpl_vars)



    def _index(self):
        tpl_vars = {}
        tpl_vars['host_eui64'] = self._bridge.host_eui64_hex
        tpl_vars['system_version'] = self._ver.version_string
        tpl_vars['system_ember_firmware'] = self._ver.firmware_version
        tpl_vars['system_mac_address'] = self._ver.mac_address
        tpl_vars['system_ncp_version'] = self._ver.ncp_stack_version
        if self._wdm.watchdog_enabled:
            tpl_vars['watchdog_status'] = 'enabled'
        else:
            tpl_vars['watchdog_status'] = 'disabled'
        monitored_keys = self._wdm.watchdog_keys
        watchdog_key_table = ''
        for k in monitored_keys:
            if time.time() - monitored_keys[k] < watchdog_monitor.WatchdogMonitor.WATCHDOG_MAX_INTERVAL:
                watchdog_key_table = watchdog_key_table + '<tr><td>%s</td><td><span class="label label-success">%1d</span></td></tr>' % (k, time.time() - monitored_keys[k])
            else:
                watchdog_key_table = watchdog_key_table + '<tr><td>%s</td><td><span class="label label-important">%1d</span></td></tr>' % (k, time.time() - monitored_keys[k])

        tpl_vars['watchdog_key_table'] = watchdog_key_table
        (eth_speed, eth_duplex, eth_auto, eth_up,) = linux_hub.get_eth_speed()
        tpl_vars['eth_speed'] = eth_speed
        tpl_vars['eth_duplex'] = eth_duplex
        tpl_vars['eth_auto'] = eth_auto
        tpl_vars['eth_up'] = eth_up
        if eth_speed == 10:
            tpl_vars['next_eth_speed'] = 100
        elif eth_speed == 100:
            tpl_vars['next_eth_speed'] = 10
        tpl_vars['command_transferring'] = self._sm.commandTransferring
        tpl_vars['command_destination_eui64'] = self._sm.commandDestinationEui64
        tpl_vars['command_tx_speed'] = self._sm.commandTransferSpeed()
        tpl_vars['command_packet_errors'] = self._sm.packetFailedCount
        tpl_vars['packet_telemetry'] = {}
        tpl_vars['device_radio_stats'] = {}
        for sourceEui64 in self._sm.loggedPacketsStatistics.keys():
            if len(self._sm.loggedPacketsStatistics[sourceEui64]) > 0:
                agg_stats = self._sm.rssiStatsForEui64(sourceEui64)
                if agg_stats != None:
                    tpl_vars['device_radio_stats'][sourceEui64] = agg_stats
                packets = [ x.to_list() for x in list(reversed(self._sm.loggedPacketsStatistics[sourceEui64])) ]
                tpl_vars['packet_telemetry'][sourceEui64] = packets

        tpl_vars['log_statements'] = self._htmlLogLines
        tpl_out = bottle.template('/usr/local/bergcloud-bridge/webassets/debug.tpl', **tpl_vars)
        return tpl_out



    def addLogRecords(self, records):
        colours = {'INFO': '#066',
         'DEBUG': '#006',
         'WARNING': '#660',
         'ERROR': '#600',
         'CRITICAL': '#600'}
        bg_colours = {'INFO': '#CFF',
         'DEBUG': '#CCF',
         'WARNING': '#FFC',
         'ERROR': '#FCC',
         'CRITICAL': '#FCC'}
        lines = []
        for record in records:
            cc = 'style="color: %s; background-color: %s"' % (colours[record.levelname], bg_colours[record.levelname])
            record_created_human_readable = time.strftime('%H:%M:%S', time.gmtime(record.created))
            html_line = '<tr><td>%s</td><td %s>%s</td><td %s>%s</td><td>%s</td></tr>' % (record_created_human_readable,
             cc,
             record.name,
             cc,
             record.levelname,
             record.message)
            lines.append(html_line)

        self._htmlLogLines += lines
        overflow = len(self._htmlLogLines) - self.limit
        if overflow > 0:
            del self._htmlLogLines[0:overflow]



    def _static_asset(self, filename):
        return bottle.static_file(filename, root='/usr/local/bergcloud-bridge/webassets/')



    def run(self):
        self._app = bottle.Bottle()
        self._route()
        self._server = InterruptableWSGIRefServer(host='', port=81)
        try:
            self._app.run(server=self._server)
        except Exception as ex:
            print ex



    def stop(self):
        self._server.stop()




class InterruptableServer(BaseHTTPServer.HTTPServer):

    def server_bind(self):
        BaseHTTPServer.HTTPServer.server_bind(self)
        self.socket.settimeout(1)
        self.run = True



    def get_request(self):
        while self.run:
            try:
                (sock, addr,) = self.socket.accept()
                sock.settimeout(None)
                return (sock, addr)
            except socket.timeout:
                if not self.run:
                    raise socket.error




    def stop(self):
        self.run = False



    def serve(self):
        while self.run:
            self.handle_request()




    def handle_error(self, request, client_address):
        logger = customlogger.Logger('webserver')
        logger.error('Error in request %s from %s' % (request, client_address))




+++ okay decompyling ./status_server.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2016.01.27 00:42:58 MSK
