# 2016.01.27 00:43:02 MSK
import time
import customlogger
import watchdogdev
from singleton import Singleton

class WatchdogMonitor(Singleton):
    WATCHDOG_MAX_INTERVAL = 60
    THREAD_WAIT_TIMEOUT = 5

    def init(self, watchdog_enabled, thread_exit_event):
        self.logger = customlogger.Logger('watchdog')
        self.watchdog_enabled = watchdog_enabled
        self.thread_exit_event = thread_exit_event
        self.watchdog_keys = {}
        self.wd = None
        if watchdog_enabled:
            self.logger.info('Initialising watchdog')
            try:
                self.wd = watchdogdev.watchdog('/dev/watchdog')
                self.logger.info('Watchdog is now open!')
            except IOError as e:
                self.logger.error('Failed to open /dev/watchdog: %s' % e)
        else:
            self.logger.warning('Watchdog not enabled')



    def updateKey(self, key):
        if not hasattr(self, 'watchdog_keys'):
            self.watchdog_keys = {}
        self.watchdog_keys[key] = time.time()



    def keys(self):
        return self.watchdog_keys



    def patWatchdog(self):
        if not self.wd:
            return 
        event_state = self.thread_exit_event.wait(WatchdogMonitor.THREAD_WAIT_TIMEOUT)
        while not event_state:
            pat = True
            for k in self.watchdog_keys.keys():
                if time.time() - self.watchdog_keys[k] > WatchdogMonitor.WATCHDOG_MAX_INTERVAL:
                    self.logger.warning('Oh no! Watchdog key %s is over interval!' % k)
                    pat = False

            if pat == True:
                self.wd.keep_alive()
            event_state = self.thread_exit_event.wait(WatchdogMonitor.THREAD_WAIT_TIMEOUT)

        self.shutdown()



    def shutdown(self):
        self.logger.info('Shutting down watchdog')
        self.watchdog_enabled = False
        if self.wd:
            self.wd.magic_close()
            self.wd = None




+++ okay decompyling ./watchdog_monitor.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2016.01.27 00:43:02 MSK
