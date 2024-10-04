#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
################################################################################
About Path(File, Directory, Link etc)
################################################################################
"""

import os
import ctypes

from minghu6.etc.version import iswin


def isemptyfile(fn):
    with open(fn, "rb") as f:
        length = len(f.read(1))
    return length == 0


def isemptydir(fn):
    return os.listdir(fn).__len__() == 0


def add_postfix(fn, postfix, sep="_"):
    name, ext = os.path.splitext(fn)

    return "".join([name, sep, postfix, ext])


def get_drivers():
    if not iswin():
        raise OSError("only support in Windows")

    lp_buffer = ctypes.create_string_buffer(78)
    ctypes.windll.kernel32.GetLogicalDriveStringsA(ctypes.sizeof(lp_buffer), lp_buffer)
    drivers = lp_buffer.raw.split(b"\x00")

    return [
        each_driver.decode()[:2]
        for each_driver in drivers
        if each_driver and os.path.isdir(each_driver)
    ]


class DirectoryConflicts(Exception):
    pass


def ensure_dir_exists(path):
    if not os.path.isdir(path):
        if os.path.lexists(path):  # broken link is True
            raise DirectoryConflicts(path)
        else:
            os.makedirs(path)


def path_level(path):
    """
    >>> path_level('/home/john')
    2
    >>> path_level('/home/john/')
    3
    """

    def _path_level(path, n=0):
        dir_path = os.path.dirname(path)
        if path == dir_path:
            return n
        else:
            n += 1
            return _path_level(dir_path, n)

    return _path_level(path)


def is_relative_path(path):
    """don't care about if the path exists"""
    if iswin():
        if not os.path.splitdrive(path)[0]:
            return False
        else:
            return True
    else:
        if path.startswith("/"):
            return False
        else:
            return True
