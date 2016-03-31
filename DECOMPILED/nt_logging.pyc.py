# 2016.01.27 00:42:51 MSK
import ctypes
import logging
import os
import re

class StreamHandler(logging.StreamHandler):

    @property
    def is_tty(self):
        isatty = getattr(self.stream, 'isatty', None)
        return isatty and isatty()



    def emit(self, record):
        try:
            message = self.format(record)
            stream = self.stream
            if not self.is_tty:
                stream.write(message)
            else:
                self.output_colorized(message)
            stream.write(getattr(self, 'terminator', '\n'))
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise 
        except:
            self.handleError(record)


    ansi_esc = re.compile('\\x1b\\[((\\d+)(;(\\d+))*)m')
    nt_color_map = {0: 0,
     1: 4,
     2: 2,
     3: 6,
     4: 1,
     5: 5,
     6: 3,
     7: 7}

    def output_colorized(self, message):
        parts = self.ansi_esc.split(message)
        write = self.stream.write
        h = ctypes.windll.kernel32.GetStdHandle(-11)
        while parts:
            text = parts.pop(0)
            if text:
                write(text)
            if len(parts) > 4:
                params = parts[0]
                parts = parts[4:]
                if h is not None:
                    params = [ int(p) for p in params.split(';') ]
                    color = 0
                    for p in params:
                        if 40 <= p <= 47:
                            color |= self.nt_color_map[(p - 40)] << 4
                        elif 30 <= p <= 37:
                            color |= self.nt_color_map[(p - 30)]
                        elif p == 1:
                            color |= 8
                        elif p == 0:
                            color = 7

                    ctypes.windll.kernel32.SetConsoleTextAttribute(h, color)





+++ okay decompyling ./nt_logging.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2016.01.27 00:42:51 MSK
