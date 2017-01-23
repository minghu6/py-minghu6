# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""

from io import StringIO
from contextlib import redirect_stdout

def test_print_num():
    from minghu6.algs.pprint import print_num
    result = print_num(10000000000, split_len=3,split_char='_', need_print=False)
    assert result == '10_000_000_000'



if __name__ == '__main__':
    test_print_num()