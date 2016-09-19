# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""
get proxy ip in china high anonymous
(need lxml(c-dependencies) or beautifulsoup4(pure python))
"""

import urllib.request
import urllib.error
import time
import datetime
from lxml import etree
import sqlite3,time
import traceback
from argparse import ArgumentParser

from minghu6.http.request import headers
from minghu6.internet.proxy_ip import proxy_ip


def main(loop=None,
         dbname=None, # None means connect to reserved db
         check=False,
         getip=False,
         delete=False,
         ip_port=(),
         debug=False):


    proxy = proxy_ip(dbname=dbname, debug=debug)

    if loop != None:
        proxy.loop(loop)

    elif getip:
        ipset = proxy.get_ip_port(region='%')

        for ip, port in ipset:
            print(ip, port)

    elif check:
        proxy.check_db_pool()

    elif delete:
        proxy.delete_db(*ip_port)

    pass


def interactivre():
    from argparse import ArgumentParser

    parser = ArgumentParser(prog='proxy_ip')

    parser.add_argument('-loop', type=int,
                        help='start loop, get pages from server (default 2)')

    parser.add_argument('-db', '--dbname', default=None,
                        help=('point dbname to connect '
                              '(default is ...  minghu6_py/resources/proxy.db)'
                              'WARNNING: the name of `proxy.db` is RESERVED'))

    parser.add_argument('-check', action='store_true',
                        help='check the db pool, judge if isAlive')


    parser.add_argument('-getip', action='store_true',
                        help='get all proxy ip port')

    parser.add_argument('-del', '--delete', action='store_true',
                        help='{0} -del ip port'.format(proxy_ip))

    parser.add_argument('ip_port', nargs='*',
                        help='suplly ip port')

    parser.add_argument('-debug', '--debug', action='store_true',
                        help='run with debug pattern')



    args = parser.parse_args().__dict__

    main(**args)

if __name__ == '__main__':

    interactivre()


