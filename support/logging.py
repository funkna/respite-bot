import enum
import os
import sys
import time

class Logger:

    class LogLevelEnum(enum.Enum):
        CONSOLE = 0
        FILE = 1

    _log_filename = 'respite.log'

    @staticmethod
    def log(msg, log_level=LogLevelEnum.FILE):
        t = time.localtime()
        f_msg = f'[{t.tm_year}/{t.tm_mon}/{t.tm_mday} {t.tm_hour}:{t.tm_min}:{t.tm_sec}] {msg}'

        if log_level.value >= Logger.LogLevelEnum.CONSOLE.value:
            print(f_msg)

        if log_level.value >= Logger.LogLevelEnum.FILE.value:
            try:
                with open(Logger._log_filename, 'a') as log_file:
                    log_file.write(str(f_msg.encode('utf-8')))
                    log_file.write('\n')
            except:
                print(f"Couldn't log: {f_msg} {str(f_msg.encode('utf-8'))}")
