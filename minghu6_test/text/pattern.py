# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""
import re

def ipv4_simple_test():
    from minghu6.text.pattern import ipv4_simple

    raw_text = '''abcdefg1234567333.555..67.你好http://344.112.1.11111111
    123.221.221.1sdsdaasdefxsdd哈哈 123.221.221.2 sdsds哈哈
    '''

    assert re.search(ipv4_simple, raw_text).group(0) == '123.221.221.2'


def han_test():
    from minghu6.text.pattern import han
    from minghu6.text.pattern import hans


    raw_text = '''    <tr class="">
      <td class="country"><img src="./国外高匿免费HTTP代理IP_国外高匿_files/nz.png" alt="Nz"></td>
      <td>121.73.141.246</td>
      <td>21320</td>
      <td>
        新西兰
      </td>
      <td class="country">高匿</td>
      <td>HTTP</td>
      <td class="country">
        <div title="6.423秒" class="bar">
          <div class="bar_inner slow" style="width:58%">'''

    ihans = '{0}+'.format(han)

    assert re.search(ihans, raw_text).group(0) == '国外高匿免费'
    assert re.search(hans, raw_text).group(0) == '国外高匿免费'

if __name__ == '__main__':

    ipv4_simple_test()
    han_test()