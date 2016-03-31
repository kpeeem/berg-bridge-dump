# 2016.01.27 00:42:56 MSK
import urllib2
import json
import time
import os
import sys
import re
import customlogger
STATS_URL = 'http://10.10.34.5:3001/post_statistics'
cached_hostname = None

def makeStatHash(name, number):
    global cached_hostname
    if cached_hostname == None:
        with file('/proc/sys/kernel/hostname') as fp:
            cached_hostname = fp.read().rstrip()
    return {'source': cached_hostname,
     'name': name.strip().lower(),
     'number': number}



def postStats(statsArray):
    print 'statsd posting %d stats' % len(statsArray)
    data = json.dumps({'statistics': statsArray})
    req = urllib2.Request(STATS_URL, data, {'Content-Type': 'application/json'})
    f = urllib2.urlopen(req)
    response = f.read()
    f.close()



def getPSSForPID(pid):
    with file('/proc/%s/smaps' % pid) as fp:
        return sum([ int(x) for x in re.findall('^Pss:\\s+(\\d+)', fp.read(), re.M) ])



def getNameForPID(pid):
    with file('/proc/%s/status' % pid) as fp:
        elems = fp.readline().split(':')
        return elems[1].strip()



def getMeminfo():
    stats = []
    with open('/proc/meminfo', 'r') as f:
        lines = f.readlines()
        for l in [ l.split(':') for l in lines ]:
            (val, size,) = l[1].split()
            stats.append(makeStatHash('meminfo-' + l[0], val))

    return stats



def getProcInfo(pid, prefix):
    stats = []
    with open('/proc/%s/statm' % pid, 'r') as f:
        s = f.read().strip().split()
        stats.append(makeStatHash('%s-process-size' % prefix, s[0]))
        stats.append(makeStatHash('%s-resident-size' % prefix, s[1]))
    return stats



def getUptime():
    stats = []
    with open('/proc/uptime', 'r') as f:
        s = f.read().strip().split()
        stats.append(makeStatHash('system-uptime', s[0]))
        stats.append(makeStatHash('system-idletime', s[1]))
    return stats



def allPIDs():
    pids = []
    for pid in filter(lambda x: x.isdigit(), os.listdir('/proc')):
        pids.append(pid)

    return pids



def collectAndPostAll():
    logger = customlogger.Logger('statsd')
    try:
        stats = getMeminfo()
        stats.extend(getUptime())
        for pid in allPIDs():
            try:
                pss = getPSSForPID(pid)
                procName = getNameForPID(pid)
                if procName == 'python':
                    stats.extend(getProcInfo(pid, 'weminuche'))
                stat = makeStatHash('process-%s-pss' % procName, pss)
                stats.append(stat)
            except:
                pass

        postStats(stats)
    except:
        logger.exception('Unexpected statsd thread error:', sys.exc_info())


if __name__ == '__main__':
    while True:
        collectAndPostAll()
        time.sleep(60)


+++ okay decompyling ./statsd.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2016.01.27 00:42:57 MSK
