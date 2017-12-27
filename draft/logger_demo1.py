# coding: utf-8
import logging
default_logger = logging.getLogger('default_logger')
fh = logging.FileHandler('test.log', mode='a', encoding='utf8', delay=False)
default_logger.addHandler(fh)
default_logger.isEnabledFor(logging.INFO)
default_logger.setLevel(logging.INFO)
default_formatter = logging.Formatter('%(asctime)-15s %(levelname)s %(process)d %(processName)-8s %(message)s')
fh.setFormatter(default_formatter)

import logging.handlers as handlers

trh = handlers.TimedRotatingFileHandler('time_rotating_handler_test.log', when='D', interval=1)
default_logger.addHandler(trh)
