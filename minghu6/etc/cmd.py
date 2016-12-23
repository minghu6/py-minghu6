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
from minghu6.etc.env import get_env_var_sep
from minghu6.etc.path import chdir
from minghu6.algs.ordered_set import OrderedSet

def search(curdir, input_s):
    """
    use to autocomplete
    ## the 'f' does not exist
    #    input_s           dirname           basename
    # 1. d:\codind\f       d:\coding         f
    # 2. d:\coding\file\   d:\coding\file    ''
    # 3. file              ''                file
    # 4. d:\coding\file    d:\coding         file
    # 5. file\             file              ''
    # 6. f                 ''                f

    :param curdir:
    :param input_s:
    :return:
    """

    dir = os.path.dirname(input_s)
    base = os.path.basename(input_s)
    with chdir(curdir):
        if os.path.exists(dir): # 1. 2. 4. 5.
            # start search in thr dir
            all_set = set(os.listdir(dir))

        else: # 3. 6.
            all_set = set(os.listdir(curdir)).union(find_global_exec_file())

    match_list = []
    match_list = [item for item in all_set if item.startswith(base)]
    match_list = sorted(match_list, key =lambda key: len(key))
    #print(match_set)
    if len(set(match_list)) != 1: # approxiamate matching, ignore case
        match_ignore_case_list = []
        for item in all_set:
            if item.lower().startswith(base.lower()):
                match_ignore_case_list.append(item)


        match_ignore_case_list = sorted(match_ignore_case_list,
                                       key =lambda key: len(key))

        #print(match_ignore_case_set)
        match_set = OrderedSet(match_list + match_ignore_case_list)
    else:
        match_set = OrderedSet(match_list)


    return match_set

def find_exec_file(path):
    exec_file_list = []
    for file in os.listdir(path):
        if iswin():
            if os.path.splitext(file)[1] == '.exe':
                exec_file_list.append(os.path.splitext(file)[0])
        else:
            if os.access(os.path.join(path, file), os.X_OK):
                exec_file_list.append(os.path.splitext(file)[0])

    return exec_file_list

def find_global_exec_file():

    path_str = os.getenv('PATH')
    env_var_sep = get_env_var_sep()
    path_list = path_str.split(env_var_sep)

    global_exec_file_list = []
    for path in path_list:
        global_exec_file_list.extend(find_exec_file(path))

    return set(global_exec_file_list)
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


