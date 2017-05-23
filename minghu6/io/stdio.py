# -*- coding:utf-8 -*-
# !/usr/bin/env python3

"""
################################################################################
About stdard io
################################################################################
"""
import os

from minghu6.etc.version import ispython2

__all__ = ['askoverride',
           'askyesno',
           ]


def askyesno(prompt='', end='(y/n)', default=None, **kwargs):
    if ispython2():
        global input
        input = raw_input
    value = input(prompt + end).strip().upper()
    if value in ('Y', 'YES') or (not value and default):
        return True
    elif value in ('N', 'NO') or (not value and default):
        return False
    else:
        return askyesno(prompt=prompt, end=end, default=default)


def askoverride(fn, default=None, print_func=print, **kwargs):
    fn = os.path.realpath(fn)

    if os.path.exists(fn):
        end = '(y/n)'
        default_ask = None
        if default == True:
            end = '(Y/n)'
            default_ask = True
        elif default == False:
            end = '(y/N)'
            default_ask = False

        print_func('File {0} Already Exists'.format(fn))
        return askyesno(prompt='Overreide?', end=end, default=default_ask, **kwargs)


if __name__ == '__main__':
    value = askyesno('overload the file?', default=True)
    print(value)
    print(askoverride('stdio.py'))
