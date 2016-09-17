#! /usr/bin/env python3
# -*- coding:utf-8 -*-

"""
################################################################################
reference to <Programming Python> by Mark Lutz 邮件服务器传送接口，
是email poplib smtplib模块的封装层 。
################################################################################
"""

from .mailFetcher import *
from .mailSender import *
from .mailParser import *

#当运行mail import *时，导出此处的嵌套模块

__all__='mailFetcher','mailSender','mailParser'

#自测代码在selftest.py中,使得mailconfig的路径再运行上面三个嵌套模块导入前得以设置