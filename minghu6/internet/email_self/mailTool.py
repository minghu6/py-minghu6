#! /usr/bin/env python3
# -*- coding:utf-8 -*-
"""
################################################################################
Common Super Class: be used to turn on/off Trance Info
################################################################################
"""

class MailTool:
    def trace(self,message):
        print(message)

class SilentMailTool:
    def trace(self,message):
        pass
