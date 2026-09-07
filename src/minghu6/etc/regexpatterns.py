# -*- coding:utf-8 -*-

IPV4_SIMPLE = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"

HAN = r"[\u4e00-\u9fa5]"

HANS = r"[\u4e00-\u9fa5]+"

URL = "(https?|ftp|file)://[a-zA-Z0-9+&@#/%?=~_|$!:,.;]*[a-zA-Z0-9+&@#/%=~_|$]"

URL_NET = "(https?|ftp)://[a-zA-Z0-9+&@#/%?=~_|$!:,.;]*[a-zA-Z0-9+&@#/%=~_|$]"

EMAIL = "[A-Z0-9._%+-]+@[A-Z0-9.-]+\\.[A-Z]{2,6}"
