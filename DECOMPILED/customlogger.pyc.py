# 2016.01.27 00:42:36 MSK
import os
import sys
import logging
from logging import handlers
from singleton import Singleton
import traceback
import colour_formatter
import nt_logging
import Queue
if os.name == 'nt':
    LOG_PATH = 'C:\\'
else:
    LOG_PATH = '/var/log'
LOG_FULLPATH = os.path.join(LOG_PATH, 'bergcloud_bridge.log')

class QueueHandler(logging.Handler):

    def __init__(self, queue):
        logging.Handler.__init__(self)
        self.queue = queue



    def enqueue(self, record):
        try:
            self.queue.put_nowait(record)
        except Queue.Full:
            pass



    def prepare(self, record):
        self.format(record)
        record.msg = record.message
        record.args = None
        record.exc_info = None
        return record



    def emit(self, record):
        try:
            self.enqueue(self.prepare(record))
        except (KeyboardInterrupt, SystemExit):
            raise 
        except:
            self.handleError(record)




class LoggerManager(Singleton):

    def init(self, daemon_mode = False, logfile_mode = False, logging_queue = False):
        self.root_logger = logging.getLogger()
        self.logfile_handler = None
        self.stream_handler = None
        self.logging_queue = None
        self.root_logger.setLevel(logging.DEBUG)
        if logfile_mode:
            if not os.path.isdir(LOG_PATH):
                try:
                    os.mkdir(LOG_PATH)
                except:
                    raise IOError('Couldn\'t create "' + LOG_PATH + '" folder. Check permissions')
            try:
                self.logfile_handler = handlers.RotatingFileHandler(LOG_FULLPATH, 'a', 262144, 0)
            except:
                raise IOError('Couldn\'t create/open file "' + LOG_FULLPATH + '". Check permissions.')
            formatter = logging.Formatter('[%(asctime)s][%(name)s %(levelname)s] %(message)s')
            self.logfile_handler.setFormatter(formatter)
            self.logfile_handler.setLevel(logging.WARNING)
            self.root_logger.addHandler(self.logfile_handler)
        if not daemon_mode:
            if os.name == 'nt':
                self.stream_handler = nt_logging.StreamHandler()
            else:
                self.stream_handler = logging.StreamHandler()
            formatter = colour_formatter.ColourFormatter('$BOLD$COLOR[%(name)s %(levelname)s]$RESET %(message)s')
            self.stream_handler.setFormatter(formatter)
            self.root_logger.addHandler(self.stream_handler)
        if logging_queue:
            self.logging_queue = logging_queue
            self.queue_handler = QueueHandler(self.logging_queue)
            self.queue_handler.setLevel(logging.WARNING)
            self.root_logger.addHandler(self.queue_handler)



    def setLoggingLevel(self, level):
        if self.root_logger != None:
            self.root_logger.setLevel(level)



    def setCloudLoggingLevel(self, level):
        if self.queue_handler != None:
            self.queue_handler.setLevel(level)



    def setFileLoggingLevel(self, level):
        if self.logfile_handler != None:
            self.logfile_handler.setLevel(level)



    def debug(self, loggername, msg):
        self.logger = logging.getLogger(loggername)
        self.logger.debug(msg)



    def info(self, loggername, msg):
        self.logger = logging.getLogger(loggername)
        self.logger.info(msg)



    def warning(self, loggername, msg):
        self.logger = logging.getLogger(loggername)
        self.logger.warning(msg)



    def error(self, loggername, msg):
        self.logger = logging.getLogger(loggername)
        self.logger.error(msg)



    def critical(self, loggername, msg):
        self.logger = logging.getLogger(loggername)
        self.logger.critical(msg)



    def exception(self, loggername, msg, exception):
        self.logger = logging.getLogger(loggername)
        (type, value, tb,) = exception
        self.logger.critical('%s - %s : %s', msg, type, value)
        stack = traceback.extract_tb(tb)
        stack.reverse()
        for line in stack:
            (filename, line_number, function_name, text,) = line
            self.logger.critical('  in file %s, line %d, function %s - %s' % (filename,
             line_number,
             function_name,
             text))





class Logger(object):

    def __init__(self, loggername = 'app'):
        self.lm = LoggerManager()
        self.loggername = loggername



    def debug(self, msg):
        self.lm.debug(self.loggername, msg)



    def info(self, msg):
        self.lm.info(self.loggername, msg)



    def warning(self, msg):
        self.lm.warning(self.loggername, msg)



    def error(self, msg):
        self.lm.error(self.loggername, msg)



    def critical(self, msg):
        self.lm.critical(self.loggername, msg)



    def exception(self, msg, exception):
        self.lm.exception(self.loggername, msg, exception)




class StdOutLogger(object):

    def __init__(self):
        self.lm = LoggerManager()



    def write(self, msg):
        self.lm.info('stdout', msg)




class StdErrLogger(object):

    def __init__(self):
        self.lm = LoggerManager()



    def write(self, msg):
        pass




+++ okay decompyling ./customlogger.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2016.01.27 00:42:37 MSK
