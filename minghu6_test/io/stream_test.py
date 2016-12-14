# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""
from minghu6.io import stream

def hexStr_bytesIter_test():

    s = 'FFD8FF'
    bytes_iter = stream.hexStr_bytesIter(s)
    assert list(bytes_iter) == [255, 216, 255]


if __name__ == '__main__':

    hexStr_bytesIter_test()
