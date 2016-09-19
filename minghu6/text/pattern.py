# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""
 supply some regrex pattern， so that we can recombinate them
"""
import re

ipv4_simple = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"

han = r"[\u4e00-\u9fa5]"

hans = r"[\u4e00-\u9fa5]+"


