# -*- Coding:utf-8 -*-
#!/usr/bin/env python3

"""
################################################################################
Command will be execute
################################################################################
"""

from subprocess import Popen

from subprocess import PIPE
from subprocess import CREATE_NEW_CONSOLE


from minghu6.text.encoding import get_locale_codec


def exec_cmd(cmd,shell=True):
    """
    only can be used in shell
    :param cmd:" " or []
    :param shell: default True
    :return: [str1,str2,...]
    """
    p = Popen(cmd,stdout=PIPE,creationflags = CREATE_NEW_CONSOLE,shell=shell)

    codec=get_locale_codec()

    lines = []
    for line in p.stdout.readlines():
        try:
            line = line.decode(codec)
        except UnicodeDecodeError:
            codec='utf-8'
            line = line.decode(codec)
        finally:
            lines.append(line)

    return lines

if __name__ == '__main__':
    from minghu6.etc.version import iswin,islinux
    s=''
    if iswin():
        s=''.join(exec_cmd('dir'))
    elif islinux():
        s=''.join(exec_cmd('ls'))

    print(s)
