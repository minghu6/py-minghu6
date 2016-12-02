# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""


User_Agent_mobile = ('Mozilla/5.0 (iPhone;CPU iPhone OS 7_1_2 like Mac OS X)'
                     'AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257'
                     'Safari/9537.53')

User_Agent = ('Mozilla/5.0(Windows NT 6.3)'
              'AppleWebKit/537.36 (KHTML,like Gecko)'
              'Chrome/39.0.2171.95'
              'Safari/537.36')

Accept = ('text/html,application/xhtml+xml,'
                   'application/xml;'
                   'q=0.9,image/webp,*/*;q=0.8')

headers={'User-Agent':User_Agent,
         'Accept':Accept,
         'Connection':'keep-alive',}

headers_mobile = {'User-Agent':User_Agent_mobile,
                  'Accept':Accept,
                  'Connection':'keep-alive',}

if __name__ == '__main__':

    print(headers_mobile)