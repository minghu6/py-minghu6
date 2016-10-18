#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
################################################################################
pprint: for beautiful and readable print
################################################################################
"""
from pprint import pprint

def print_num(num,split_len=3,split_char=' ',need_print=True):
    """
    Example:
        print_num(1000000000000000,split_char='_',split_len=3)
        '1_000_000_000_000_000'
    :param num:
    :param split_len:
    :param split_char:
    :return:formatted str
    """
    assert split_len>0

    l=[c+split_char  if (i)%split_len==0 else c for i,c in enumerate(reversed(str(num)))]
    snum=''.join(l[::-1])[:-1]
    if need_print:
        pprint(snum)
    return snum

if __name__ == '__main__':
    print_num(10000000000, split_len=3,split_char='_')