# -*- Coding:utf-8 -*-
# !/usr/bin/env python3

"""
################################################################################
Command will be execute
################################################################################
"""

import os
import sys
import re
import threading
from contextlib import contextmanager
from distutils.version import LooseVersion
from threading import Thread
from subprocess import Popen, PIPE

from minghu6.text.encoding import get_locale_codec

__all__ = ['exec_cmd',
           'search', 'find_exec_file', 'find_global_exec_file',
           'has_proper_chromedriver',
           'has_proper_geckodriver',
           'has_proper_ffmpeg',
           'has_proper_git',
           'has_proper_java',
           'has_proper_tesseract',
           'CommandRunner']


@contextmanager
def chdir(path):
    with threading.Lock():
        oldpath = os.path.abspath(os.curdir)
        try:

            os.chdir(path)
            yield None

        finally:
            os.chdir(oldpath)


def get_env_var_sep():
    if iswin():
        return ';'
    else:
        return ':'  # Linux, Unix, OS X


def exec_cmd(cmd, shell=True):
    """
    only can be used in shell
    :param cmd:" " or []
    :param shell: default True
    :return: [str1,str2,...]
    """
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=shell)

    stdout_data, stderr_data = p.communicate()

    codec = get_locale_codec()

    try:
        stdout_data = stdout_data.decode(codec, errors='ignore')
        stderr_data = stderr_data.decode(codec, errors='ignore')
    except UnicodeDecodeError:
        codec = 'utf-8'
        stdout_data = stdout_data.decode(codec, errors='ignore')
        stderr_data = stderr_data.decode(codec, errors='ignore')

    finally:
        info, err = stdout_data.split(os.linesep), stderr_data.split(os.linesep)

    return info, err


try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty  # python 3.x


class CommandRunner(object):
    """Inspired by https://stackoverflow.com/questions/375427/non-blocking-read-on-a-subprocess-pipe-in-python"""
    ON_POSIX = 'posix' in sys.builtin_module_names
    
    @classmethod
    def _enqueue_output(cls, process, out, queue):
        for line in iter(out.readline, b''):
            queue.put(line)
        
        process.terminate()
        process.poll()
    
    @classmethod
    def run(cls, cmd):
        if isinstance(cmd, list):
            cmd = ' '.join(cmd)
        
        p = Popen('{cmd} && exit'.format(cmd=cmd), stdout=PIPE, stderr=PIPE, bufsize=1,
                  close_fds=CommandRunner.ON_POSIX, shell=True)
        q = Queue()
        t_stdout = Thread(target=CommandRunner._enqueue_output, name='{cmd} fetch stdout'.format(cmd=cmd),
                          args=(p, p.stdout, q), daemon=True)
        t_stderr = Thread(target=CommandRunner._enqueue_output, name='{cmd} fetch stderr'.format(cmd=cmd),
                          args=(p, p.stderr, q), daemon=True)
        
        t_stdout.start()
        t_stderr.start()
        
        # read line without blocking
        codec = get_locale_codec()
        while p.returncode is None:
            try:
                line = q.get(timeout=.1)
                line = line.strip().decode(codec, errors='ignore')
            except Empty:
                pass
            else:  # got line
                yield line


################################################################################
from ordered_set import OrderedSet


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
        if os.path.exists(dir):  # 1. 2. 4. 5.
            # start search in thr dir
            all_set = set(os.listdir(dir))

        else:  # 3. 6.
            all_set = set(os.listdir(curdir)).union(find_global_exec_file())

    match_list = [item for item in all_set if item.startswith(base)]
    match_list = sorted(match_list, key=lambda key: len(key))
    # print(match_set)
    if len(set(match_list)) != 1:  # approxiamate matching, ignore case
        match_ignore_case_list = []
        for item in all_set:
            if item.lower().startswith(base.lower()):
                match_ignore_case_list.append(item)

        match_ignore_case_list = sorted(match_ignore_case_list,
                                        key=lambda key: len(key))

        # print(match_ignore_case_set)
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
class DoNotHaveProperVersion(BaseException): pass


def has_proper_git(max_version=None, min_version=None):
    version_pattern = '((\d)+\.)+'

    info_lines, err_lines = exec_cmd('git --version')
    if len(err_lines) >= 1 and err_lines[0] != '':
        return False

    m = re.search(version_pattern, info_lines[0])
    v = LooseVersion(m.group())
    if max_version is not None:
        if v >= LooseVersion(max_version):
            return False
    if min_version is not None:
        if v < LooseVersion(min_version):
            return False

    return True


def has_proper_java(min_version=None):
    info_lines, err_lines = exec_cmd('java -version')

    # java output stream is stderr !!!
    if len(err_lines) == 0:
        return False

    if min_version is not None:
        v1 = LooseVersion(min_version)

        pattern = r"(\d+.){2}\d+"
        result = re.search(pattern, err_lines[0]).group(0)
        v2 = LooseVersion(result)

        return v1 <= v2

    return True


def has_proper_tesseract(min_version=None):
    min_version = None
    info_lines, err_lines = exec_cmd('tesseract -v')

    # java output stream is stderr !!!
    if len(info_lines) == 0:
        return False

    if min_version is not None:
        v1 = LooseVersion(min_version)

        pattern = r"(\d+.){2}\d+"
        result = re.search(pattern, info_lines[0]).group(0)
        v2 = LooseVersion(result)

        return v1 <= v2

    return True


def has_proper_ffmpeg():
    _, err_lines = exec_cmd('ffmpeg -version')

    if len(err_lines) >= 1 and err_lines[0] != '':
        return False
    else:
        return True


def has_proper_ffprobe():
    _, err_lines = exec_cmd('ffprobe -version')

    if len(err_lines) >= 1 and err_lines[0] != '':
        return False
    else:
        return True


def has_proper_chromedriver():
    info_lines, err_lines = exec_cmd('chromedriver --version')
    if err_lines:
        return False

    version = info_lines[0].split(' ')[1].split()
    return True


def has_proper_geckodriver():
    info_lines, err_lines = exec_cmd('chromedriver --version')
    if err_lines:
        return False

    version = info_lines[0].split(' ')[1].split()
    # print(version)
    return True


if __name__ == '__main__':
    from minghu6.etc.version import iswin, islinux

    s = ''
    if iswin():
        s = '\n'.join(exec_cmd('dir')[0])
    elif islinux():
        s = '\n'.join(exec_cmd('ls')[0])

    print(s)
