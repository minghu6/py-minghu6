#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import platform
import sys

__all__ = [
    "iswin",
    "islinux",
    "ispython2",
    "ispython3",
]


def iswin():
    return platform.platform().upper().startswith("WIN")


def islinux():
    return platform.platform().upper().startswith("LINUX")


def ispython2():
    return sys.version_info.major == 2


def ispython3():
    return sys.version_info.major == 3


if __name__ == "__main__":
    print(os.curdir)
