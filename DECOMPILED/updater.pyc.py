# 2016.01.27 00:42:59 MSK
import os
import optparse
import urllib2
import urllib
import httplib
import socket
import ssl
import subprocess
import_failed = False
try:
    import version
    import linux_hub
except:
    import_failed = True
UPDATE_SERVER = 'bridge-updates.bergcloud.com'
UPDATE_PORT = 443
SFTP_KEY = '/etc/ssh_host_dsa_key'
SFTP_USER = 'rescue'
SFTP_RESCUE_PACKAGE = 'weminuche_bridge_rescue_A.ipk'
SSL_KEY = '/etc/ssl/private/bridge-update-client.key'
SSL_CERT = '/etc/ssl/certs/bridge-update-client.crt'
SSL_CA_PEM = '/etc/ssl/ca/cacert.pem'

def fetch_ssl(outputfile):
    try:
        model_number = urllib.quote(version.Version.BRIDGE_HARDWARE_MODEL)
        current_build = version.Version.BRIDGE_BUILD_VERSION
        current_version = urllib.quote('%d.%d.%d' % (version.Version.BRIDGE_MAJOR_VERSION, version.Version.BRIDGE_MINOR_VERSION, version.Version.BRIDGE_MAINT_VERSION))
        mac_address = linux_hub.get_mac('eth0')
        if mac_address:
            mac_address = mac_address.replace(':', '%3A')
        if UPDATE_PORT == 443:
            protocol = 'https'
            handler = VerifiedHTTPSHandler()
        else:
            protocol = 'http'
            handler = urllib2.HTTPHandler()
        url = '%s://%s:%d/firmware/autoupdate?model=%s&mac_address=%s&version=%s&build=%s' % (protocol,
         UPDATE_SERVER,
         UPDATE_PORT,
         model_number,
         mac_address,
         current_version,
         current_build)
        opener = urllib2.build_opener(handler)
        response = opener.open(url)
        with open('%s' % outputfile, 'wb') as f:
            f.write(response.read())
        print 'Finished!'
    except urllib2.URLError as url_error:
        if hasattr(url_error, 'getcode') and url_error.getcode() == 404:
            print 'No updates'
        else:
            print 'URLError: ',
            print url_error
    except urllib2.HTTPError as http_error:
        print 'HTTPError: ',
        print http_error.read()



def fetch_ssh(outputfile):
    import subprocess
    p = subprocess.Popen(['sftp',
     '-i',
     SFTP_KEY,
     '-o StrictHostKeyChecking=no',
     '-o UserKnownHostsFile=/dev/null',
     '%s@%s:%s' % (SFTP_USER, UPDATE_SERVER, SFTP_RESCUE_PACKAGE),
     outputfile], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    print 'sftp stdout: %s' % repr(p.stdout.read())
    print 'sftp stderr: %s' % repr(p.stderr.read())



def main(outputfile):
    if import_failed:
        print 'Import failed. Fetching SSH copy'
        fetch_sftp(outputfile)
    else:
        fetch_ssl(outputfile)



class VerifiedHTTPSConnection(httplib.HTTPSConnection):

    def __init__(self, *args, **kwargs):
        httplib.HTTPSConnection.__init__(self, *args, **kwargs)
        self.timeout = 30



    def connect(self):
        sock = socket.create_connection((self.host, self.port), self.timeout)
        if self._tunnel_host:
            self.sock = sock
            self._tunnel()
        self.sock = ssl.wrap_socket(sock, SSL_KEY, SSL_CERT, cert_reqs=ssl.CERT_REQUIRED, ca_certs=SSL_CA_PEM)




class VerifiedHTTPSHandler(urllib2.HTTPSHandler):

    def __init__(self, connection_class = VerifiedHTTPSConnection):
        self.specialized_conn_class = connection_class
        urllib2.HTTPSHandler.__init__(self)



    def https_open(self, req):
        return self.do_open(self.specialized_conn_class, req)



if __name__ == '__main__':
    subprocess.call(['mount',
     '-o',
     'remount,rw',
     '/'])
    parser = optparse.OptionParser()
    parser.add_option('--outputfile', action='store', type='string', dest='outputfile', help='Patch output filename')
    (options, args,) = parser.parse_args()
    if len(options.outputfile) > 0 and options.outputfile and os.path.isdir(os.path.dirname(options.outputfile)):
        main(options.outputfile)
    else:
        print 'Please specify a valid output filename with --outputfile, and ensure the enclosing directory exists'
        sys.exit(1)

+++ okay decompyling ./updater.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2016.01.27 00:43:01 MSK
