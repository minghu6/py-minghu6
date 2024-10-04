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
import logging
import tempfile
import platform
import signal
import time
from contextlib import contextmanager
from packaging.version import Version
from threading import Thread
from queue import Queue, Empty
from subprocess import Popen, PIPE


from minghu6.etc.version import iswin
from ..data.userstr import CustomBytes


@contextmanager
def mkstempfile(suffix=None, prefix=None, dir=None, text=False):
    _fd, fpath = tempfile.mkstemp(suffix=suffix, prefix=prefix, dir=dir, text=text)

    try:
        yield fpath
    finally:
        if os.path.exists(fpath):
            os.remove(fpath)


if platform.platform().upper().startswith("WIN"):
    ENV_SEP = ";"
else:
    ENV_SEP = ":"


def get_locale_codec():
    """
    Is Very Very Useful
    :return:
    """
    import locale
    import codecs

    return codecs.lookup(locale.getpreferredencoding()).name


def alarm(timeout):
    if iswin():

        class _Alarm(Thread):
            def __init__(self, timeout):
                Thread.__init__(self)
                self.timeout = timeout
                self.setDaemon(True)

            def run(self):
                self._run()

            def _run(self):
                time.sleep(self.timeout)
                # raise TimeoutError('%.2f (s) timeout'%self.timeout)

                os._exit(0)

        def exit_handle(signal, frame):
            raise TimeoutError

        signal.signal(signal.SIGINT, exit_handle)

        alarm = _Alarm(timeout)
        alarm.start()
        del alarm

    else:
        from signal import alarm

        def timeout_handle(signal, frame):
            raise TimeoutError

        signal.signal(signal.SIGINT, timeout_handle)

        alarm(timeout)


def exec_cmd(cmd, shell=True):
    """
    only can be used in shell (`exec_cmd("ffmpeg -version")`)
    """
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=shell)

    stdout_data, stderr_data = p.communicate()

    codec = get_locale_codec()

    try:
        stdout_data = stdout_data.decode(codec, errors="ignore")
        stderr_data = stderr_data.decode(codec, errors="ignore")
    except UnicodeDecodeError:
        codec = "utf-8"
        stdout_data = stdout_data.decode(codec, errors="ignore")
        stderr_data = stderr_data.decode(codec, errors="ignore")

    finally:
        info, err = stdout_data.split(os.linesep), stderr_data.split(os.linesep)

    return info, err


class CommandRunner(object):
    """Inspired by https://stackoverflow.com/questions/375427/non-blocking-read-on-a-subprocess-pipe-in-python"""

    ON_POSIX = "posix" in sys.builtin_module_names

    @classmethod
    def _enqueue_output(cls, process, out, queue):
        for line in iter(out.readline, b""):
            line = CustomBytes(line)

            if out is process.stdout:
                line.extra_attrs["tag"] = "stdout"
            elif out is process.stderr:
                line.extra_attrs["tag"] = "stderr"

            queue.put(line)

        while True:
            if process.poll() is not None:
                process.terminate()
                break

    @classmethod
    def run(cls, cmd):
        if isinstance(cmd, list):
            cmd = " ".join(cmd)

        p = Popen(
            "{cmd} && exit".format(cmd=cmd),
            stdout=PIPE,
            stderr=PIPE,
            close_fds=CommandRunner.ON_POSIX,
            shell=True,
        )
        q = Queue()
        t_stdout = Thread(
            target=CommandRunner._enqueue_output,
            name="{cmd} fetch stdout".format(cmd=cmd),
            args=(p, p.stdout, q),
            daemon=True,
        )
        t_stderr = Thread(
            target=CommandRunner._enqueue_output,
            name="{cmd} fetch stderr".format(cmd=cmd),
            args=(p, p.stderr, q),
            daemon=True,
        )

        t_stdout.start()
        t_stderr.start()

        # read line without blocking
        codec = get_locale_codec()
        while p.returncode is None:
            try:
                line = q.get(timeout=0.1)
                line = line.strip().decode(codec, errors="ignore")
            except Empty:
                pass
            else:  # got line
                status = line.extra_attrs["tag"]
                yield status, line

    @classmethod
    def realtime_run(cls, cmd):
        print(cmd)
        if isinstance(cmd, list):
            cmd = " ".join(cmd)

        p = Popen(
            "{cmd}".format(cmd=cmd),
            stdout=sys.stdout,
            stderr=sys.stdin,
            close_fds=CommandRunner.ON_POSIX,
            shell=True,
        )

        p.wait()


def auto_resume(cmd, logdir=os.curdir, name=None, logger=None, debug=True):
    if name is None:
        name = next(tempfile._get_candidate_names()) + ".log"

    logpath = os.path.join(logdir, name)

    if logger is None:

        def _init_default_logger(logpath, debug=False):
            default_logger = logging.getLogger("default_logger")

            if debug:
                default_logger.setLevel(logging.DEBUG)
            else:
                default_logger.setLevel(logging.INFO)

            default_formatter = logging.Formatter(
                "%(asctime)-15s [%(levelname)s] %(process)-8d %(message)s"
            )

            trh = logging.handlers.TimedRotatingFileHandler(
                logpath, when="D", interval=1
            )
            trh.setFormatter(default_formatter)

            sh = logging.StreamHandler()
            sh.setFormatter(default_formatter)

            default_logger.addHandler(trh)
            default_logger.addHandler(sh)

            return default_logger

        logger = _init_default_logger(logpath, debug)

    if isinstance(cmd, list):
        cmd = " ".join(cmd)

    while True:
        is_first_line = True
        for status, line in CommandRunner.run(cmd):
            if is_first_line:
                is_first_line = False
                logger.info("start `%s`" % cmd)

            if status == "stderr":
                logger.debug(line)
            else:
                logger.warning(line)

        logger.error("found %s exit..." % cmd)


################################################################################


def find_exec_file(path):
    exec_file_list = []
    for file in os.listdir(path):
        if iswin():
            if os.path.splitext(file)[1] == ".exe":
                exec_file_list.append(os.path.splitext(file)[0])
        else:
            if os.access(os.path.join(path, file), os.X_OK):
                exec_file_list.append(os.path.splitext(file)[0])

    return exec_file_list


def find_global_exec_file():
    path_str = os.getenv("PATH")
    path_list = path_str.split(ENV_SEP)

    global_exec_file_list = []
    for path in path_list:
        global_exec_file_list.extend(find_exec_file(path))

    return set(global_exec_file_list)


################################################################################
class DoNotHaveProperVersion(Exception):
    pass


def has_proper_git(max_version=None, min_version=None):
    version_pattern = "((\\d)+\\.)+"

    info_lines, err_lines = exec_cmd("git --version")
    if len(err_lines) >= 1 and err_lines[0] != "":
        return False

    m = re.search(version_pattern, info_lines[0])
    v = Version(m.group())
    if max_version is not None:
        if v >= Version(max_version):
            return False
    if min_version is not None:
        if v < Version(min_version):
            return False

    return True


def has_proper_java(min_version=None):
    info_lines, err_lines = exec_cmd("java -version")

    # java output stream is stderr !!!
    if len(err_lines) == 0:
        return False

    if min_version is not None:
        v1 = Version(min_version)

        pattern = r"(\d+.){2}\d+"
        result = re.search(pattern, err_lines[0]).group(0)
        v2 = Version(result)

        return v1 <= v2

    return True


def has_proper_tesseract(min_version=None):
    min_version = None
    info_lines, err_lines = exec_cmd("tesseract -v")

    # java output stream is stderr !!!
    if len(info_lines) == 0:
        return False

    if min_version is not None:
        v1 = Version(min_version)

        pattern = r"(\d+.){2}\d+"
        result = re.search(pattern, info_lines[0]).group(0)
        v2 = Version(result)

        return v1 <= v2

    return True


def has_proper_ffmpeg():
    _, err_lines = exec_cmd("ffmpeg -version")

    if len(err_lines) >= 1 and err_lines[0] != "":
        return False
    else:
        return True


def has_proper_ffprobe():
    _, err_lines = exec_cmd("ffprobe -version")

    if len(err_lines) >= 1 and err_lines[0] != "":
        return False
    else:
        return True


def has_proper_chromedriver():
    info_lines, err_lines = exec_cmd("chromedriver --version")
    if err_lines:
        return False

    version = info_lines[0].split(" ")[1].split()
    return True


def has_proper_geckodriver():
    info_lines, err_lines = exec_cmd("chromedriver --version")
    if err_lines:
        return False

    version = info_lines[0].split(" ")[1].split()
    # print(version)
    return True


def askyesno(prompt="", end="(y/n)", default=None, **kwargs):
    value = input(prompt + end).strip().upper()
    if value in ("Y", "YES") or (not value and default):
        return True
    elif value in ("N", "NO") or (not value and default):
        return False
    else:
        return askyesno(prompt=prompt, end=end, default=default)


def askoverride(fn, default=None, print_func=print, **kwargs):
    fn = os.path.realpath(fn)

    if os.path.exists(fn):
        end = "(y/n)"
        default_ask = None
        if default == True:
            end = "(Y/n)"
            default_ask = True
        elif default == False:
            end = "(y/N)"
            default_ask = False

        print_func("File {0} Already Exists".format(fn))
        return askyesno(prompt="Overreide?", end=end, default=default_ask, **kwargs)


if __name__ == "__main__":
    from minghu6.etc.version import iswin, islinux

    s = ""
    if iswin():
        s = "\n".join(exec_cmd("dir")[0])
    elif islinux():
        s = "\n".join(exec_cmd("ls")[0])

    print(s)
