#! /usr/bin/env python3
# -*- coding:utf-8 -*-

"""
Thanks for mengpeng's idea
"""
__author__ = 'mengpeng'
import time


class timeme(object):
    __unitfactor = {'s': 1,
                    'ms': 1000,
                    'us': 1000000}

    def __init__(self, unit='s', precision=4):
        self.start = None
        self.end = None
        self.total = 0
        self.unit = unit
        self.precision = precision

    def __enter__(self):
        if self.unit not in timeme.__unitfactor:
            raise KeyError('Unsupported time unit.')
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time.time()
        self.total = (self.end - self.start) * timeme.__unitfactor[self.unit]
        self.total = round(self.total, self.precision)

    def __str__(self):
        return 'Running time is {0}{1}'.format(self.total, self.unit)

'''
def interactive():
    import argparse
    parser=argparse.ArgumentParser()

    parser.add_argument('exec',
                        nargs='+',
                        help=('exec arguments'))

    args=parser.parse_args()

    return args
'''

if __name__=='__main__':

    #args=interactive()
    import os
    import sys

    with timeme() as t:
        exec_str=' '.join(sys.argv[1:])
        print(exec_str)
        os.system(exec_str)

    print(t)









