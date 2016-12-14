# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""
class CanNotBeBytes(Exception):
    def __str__(self):
        return 'len(hex_str) % 2 == 0 or len(bin_str) % 8 == 0 etc.'

def hexStr_bytesIter(hexStr):
    """
    # only support hex
    :param hexStr:
    :return:
    """


    if len(hexStr) >=2 and hexStr[:2].lower() == '0x':
        hexStr = hexStr[2:]

    if len(hexStr) % 2 != 0:
        raise CanNotBeBytes

    #format(value, '0'+str(hexStr_length)+'d')

    for i in range(len(hexStr)//2):
        yield int(hexStr[i*2]+hexStr[i*2+1], 16)


