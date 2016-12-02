# -*- Coding:utf-8 -*-
#!/usr/bin/env python3

"""
################################################################################
Command will be execute
################################################################################
"""

import asyncio
from subprocess import Popen
from subprocess import PIPE
from subprocess import CREATE_NEW_CONSOLE
import re
from distutils.version import LooseVersion
import os

from minghu6.text.encoding import get_locale_codec


def exec_cmd(cmd, shell=True):
    """
    only can be used in shell
    :param cmd:" " or []
    :param shell: default True
    :return: [str1,str2,...]
    """
    p = Popen(cmd,stdout=PIPE,stderr=PIPE,shell=shell)

    stdout_data, stderr_data=p.communicate()

    codec=get_locale_codec()

    try:
        stdout_data = stdout_data.decode(codec)
        stderr_data = stderr_data.decode(codec)
    except UnicodeDecodeError:
        codec='utf-8'
        stdout_data = stdout_data.decode(codec)
        stderr_data = stderr_data.decode(codec)

    finally:
        return stdout_data.split(os.linesep)[:-1], stderr_data.split(os.linesep)[:-1]

################################################################################
class DoNotHaveProperVersion(BaseException):pass

def has_proper_git(min_version_limit=None):
    info_lines, err_lines=exec_cmd('git --version')
    if len(info_lines) == 0:
        return False

    if min_version_limit != None:
        v1 = LooseVersion(min_version_limit)

        pattern = r"(\d+.){2}\d+"
        result=re.search(pattern, info_lines[0 ]).group(0)
        v2 = LooseVersion(result)

        return v1 <= v2

    return True

def has_proper_java(min_version_limit=None):
    info_lines, err_lines=exec_cmd('java -version')

    # java output stream is stderr !!!
    if len(err_lines) == 0:
        return False

    if min_version_limit != None:
        v1 = LooseVersion(min_version_limit)

        pattern = r"(\d+.){2}\d+"
        result=re.search(pattern, err_lines[0]).group(0)
        v2 = LooseVersion(result)

        return v1 <= v2

    return True

def has_proper_tesseract(min_version_limit=None):
    min_version_limit=None
    info_lines, err_lines=exec_cmd('tesseract -v')

    # java output stream is stderr !!!
    if len(info_lines) == 0:
        return False

    if min_version_limit != None:
        v1 = LooseVersion(min_version_limit)

        pattern = r"(\d+.){2}\d+"
        result=re.search(pattern, info_lines[0]).group(0)
        v2 = LooseVersion(result)

        return v1 <= v2

    return True

def has_proper_ffmpeg():
    _, err_lines=exec_cmd('ffmpeg -version')

    return len(err_lines) == 0

if __name__ == '__main__':
    from minghu6.etc.version import iswin, islinux
    s=''
    if iswin():
        s='\n'.join(exec_cmd('dir')[0])
    elif islinux():
        s='\n'.join(exec_cmd('ls')[0])

    print(s)


