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
import re
from distutils.version import LooseVersion

from minghu6.text.encoding import get_locale_codec


def exec_cmd(cmd, shell=True):
    """
    only can be used in shell
    :param cmd:" " or []
    :param shell: default True
    :return: [str1,str2,...]
    """
    p = Popen(cmd,stdout=PIPE, stderr=PIPE,
              creationflags = CREATE_NEW_CONSOLE, shell=shell)

    codec=get_locale_codec()

    lines_stdout = []
    for line in p.stdout.readlines():
        try:
            line = line.decode(codec)
        except UnicodeDecodeError:
            codec='utf-8'
            line = line.decode(codec)
        finally:
            lines_stdout.append(line)

        lines = []

    lines_stderr = []
    for line in p.stderr.readlines():
        try:
            line = line.decode(codec)
        except UnicodeDecodeError:
            codec='utf-8'
            line = line.decode(codec)
        finally:
            lines_stderr.append(line)

    return lines_stdout, lines_stderr

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

if __name__ == '__main__':
    from minghu6.etc.version import iswin, islinux
    s=''
    if iswin():
        s=''.join(exec_cmd('dir')[0])
    elif islinux():
        s=''.join(exec_cmd('ls')[0])

    print(s)
