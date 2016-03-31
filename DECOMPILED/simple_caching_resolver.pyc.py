# 2016.01.27 00:42:52 MSK
import dns.resolver
import socket
import time
import random
import customlogger

class SimpleCachingResolver:

    def __init__(self):
        self.cache = {}
        self.logger = customlogger.Logger('resolver')
        self.r = dns.resolver.Resolver()
        self.r.timeout = 5
        servers_to_remove = []
        for ns in self.r.nameservers:
            try:
                socket.inet_aton(ns)
            except socket.error:
                servers_to_remove.append(ns)

        for ns in servers_to_remove:
            self.r.nameservers.remove(ns)

        self.r.nameservers += ['4.2.2.1', '4.2.2.2']



    def lookup(self, hostname):
        try:
            socket.inet_aton(hostname)
            self.logger.debug('Resolver given IP address %s. Returning for an hour' % hostname)
            return ([hostname], time.time() + 3600)
        except socket.error:
            return self.lookup_by_dns(hostname)



    def lookup_by_dns(self, hostname):
        try:
            (ip_address_list, expiration,) = self.cache[hostname]
            if time.time() <= expiration - 5:
                self.logger.debug('Resolver returning IPs %s from internal cache with expiry in %d s' % (ip_address_list, expiration - time.time()))
                return (list(ip_address_list), expiration)
            raise KeyError
        except KeyError:
            try:
                self.logger.debug('Looking up %s' % hostname)
                answer = self.r.query(hostname)
                expiration = answer.expiration
                dns_ip_addresses = [ a.to_text() for a in answer.rrset.items ]
                self.cache[hostname] = (dns_ip_addresses, expiration)
                self.logger.debug('Stored IP addresses %s in cache for hostname %s for %d s' % (dns_ip_addresses, hostname, expiration - time.time()))
                return (list(dns_ip_addresses), expiration)
            except:
                self.logger.error('pydns failed to look up %s, trying with system resolver' % hostname)
            try:
                result = socket.gethostbyname(hostname)
                expiration = time.time() + 86400
                dns_ip_addresses = [result]
                return (list(dns_ip_addresses), expiration)
            except:
                self.logger.error('System failed to look up %s' % hostname)
                raise 




+++ okay decompyling ./simple_caching_resolver.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2016.01.27 00:42:53 MSK
