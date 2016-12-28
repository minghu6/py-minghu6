# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""

from collections import namedtuple
from .var import isiterable, get_typename_str

class Peak:
    """
    count Peak point
    """

    def __init__(self, iterable):
        if not isiterable(iterable):
            type_name = get_typename_str(iterable)
            raise TypeError('{0} object is not iterable'.format(type_name))

        self._iterable = iterable
        self._peaks, self._start_type = Peak._compute_peaks(self._iterable)
        #print(self._peaks)


    HIGH = 'high'
    LOW = 'low'

    SORTED_ABSOLUTE_VALUE = 'absolute_value'
    SORTED_RELATIVE_DISTANCE = 'relative_distance'

    @staticmethod
    def _compute_peaks(iterable): # ignore the last item
        peaks = []
        peak_elem = namedtuple('peak_elem', ['index', 'value', 'relative_distance'])
        state = 'start'
        start_type = None

        for i, item in enumerate(iterable):

            if state == 'start':
                state = 'start-next'

            elif state == 'start-next':
                if item > last:
                    start_type = 'low'
                    state = 'up'
                elif item < last:
                    start_type = 'high'
                    state = 'down'

                peaks.append(peak_elem(i-1, last, 0)) # would be ignored then


            elif state == 'up':
                if item < last:
                    peaks.append(peak_elem(i-1, last, abs(last - peaks[-1].value)))
                    state = 'down'

                elif item == last:
                    peaks.append(peak_elem(i-1, last, abs(last - peaks[-1].value)))
                    state = 'plane'

            elif state == 'down':
                if item > last:
                    peaks.append(peak_elem(i-1, last, abs(last - peaks[-1].value)))
                    state = 'up'

                elif item == last:
                    peaks.append(peak_elem(i-1, last, abs(last - peaks[-1].value)))
                    state = 'plane'

            elif state == 'plane': # only recorde first item if item == last
                if item < last:
                    state = 'down'
                elif item > last:
                    state = 'up'

            last = item
            #print(peaks)


        return peaks[1:], start_type

    @classmethod
    def _sorted(cls, peaks, start_type, key):

        if len(peaks) == 0:
            return [], []


        if start_type == Peak.LOW:
            low_peaks = peaks[0::2]
            if len(peaks) == 1:
                high_peaks = []
            else:
                high_peaks = peaks[1::2]

        else:
            high_peaks = peaks[0::2]
            if len(peaks) == 1:
                low_peaks = []
            else:
                low_peaks = peaks[1::2]



        if key == Peak.SORTED_ABSOLUTE_VALUE:
            low_peaks = sorted(low_peaks, key= lambda x: x.value)
            high_peaks = sorted(high_peaks, key= lambda x: x.value)



        elif key == Peak.SORTED_RELATIVE_DISTANCE:
            low_peaks = sorted(low_peaks, key= lambda x: x.relative_distance, reverse=True)
            high_peaks = sorted(high_peaks, key= lambda x: x.relative_distance, reverse=True)


        return low_peaks, high_peaks


    def get_peak(self, peak_type, sorted_type=SORTED_RELATIVE_DISTANCE, most_num=None):

        if len(self._peaks) < 1:
            return []

        if peak_type == peak_type:
            res = self._peaks[0::2]
        else:
            if len(self._peaks) == 1:
                return []
            else:
                res = self._peaks[1::2]

        low_peaks, high_peaks = Peak._sorted(self._peaks, self._start_type, key=sorted_type)

        if peak_type == Peak.HIGH:
            res = high_peaks
        elif peak_type == Peak.LOW:
            res = low_peaks
        else:
            raise TypeError('{} is not valid prek_type'.format(peak_type))

        return res[slice(most_num)]