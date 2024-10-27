# -*- coding:utf-8 -*-

import datetime
from enum import Enum

from public import public

@public
class TimeUnit(Enum):
    NANO = 1
    MICRO = NANO * 1000
    MILLI = MICRO * 1000
    SEC = MILLI * 1000

    def format_long(self):
        match self:
            case self.NANO:
                return 'nanoseconds'
            case self.MICRO:
                return 'microseconds'
            case self.MILLI:
                return 'miliseconds'
            case self.SEC:
                return 'seconds'

    def format_medium(self):
        match self:
            case self.NANO:
                return 'nanos'
            case self.MICRO:
                return 'micros'
            case self.MILLI:
                return 'milis'
            case self.SEC:
                return 'secs'

    def format_short(self):
        match self:
            case self.NANO:
                return 'ns'
            case self.MICRO:
                return 'ms'
            case self.MILLI:
                return 'ms'
            case self.SEC:
                return 's'


@public
def str2datetime(s, sep="-", sep_date_time=" ") -> datetime.datetime:
    """
    input format datetime str as follow
    2017-01-02 22:12:53
    2017-01-02 22:12
    2017-01-02
    """
    all_kind_format = [
        "%Y{0}%m{0}%d".format(sep),
        "%Y-%m-%d{0}%H:%M".format(sep_date_time),
        "%Y-%m-%d{0}%H:%M:%S".format(sep_date_time),
        "%Y-%m-%d{0}%H:%M:%S.%f".format(sep_date_time),
    ]

    for one_format in all_kind_format:
        try:
            d = datetime.datetime.strptime(s, one_format)
        except ValueError:
            pass
        else:
            return d

    raise ValueError("Invalid datetime str format")

