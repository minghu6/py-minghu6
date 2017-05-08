# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""
import os
import sys
import time
import threading
import signal

from minghu6.etc.version import iswin

class _Alarm (threading.Thread):
    def __init__ (self, timeout):
        threading.Thread.__init__ (self)
        self.timeout = timeout
        self.setDaemon (True)
    def run (self):
        self._run()
    def _run(self):
        time.sleep(self.timeout)
        #raise TimeoutError('%.2f (s) timeout'%self.timeout)

        os._exit(0)

def alarm(timeout):
    if iswin():
        def exit_handle(signal, frame):
            raise TimeoutError

        signal.signal(signal.SIGINT, exit_handle)

        alarm=_Alarm(timeout)
        alarm.start()
        del alarm

    else:
        from signal import alarm
        def timeout_handle(signal, frame):
            raise TimeoutError
        alarm(timeout)
