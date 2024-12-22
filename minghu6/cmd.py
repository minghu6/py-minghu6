# -*- coding:utf-8 -*-

from ast import For
from collections.abc import Generator
from dataclasses import dataclass
import locale
import os
from pathlib import Path
from string import Template
import sys
import logging
import tempfile
import signal
import time
from contextlib import contextmanager
from threading import Thread
from queue import Queue, Empty
from subprocess import CalledProcessError, Popen, PIPE

from more_itertools import tail
from prompt_toolkit import prompt
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.formatted_text import (
    to_formatted_text,
    HTML,
    AnyFormattedText,
    FormattedText,
)

from minghu6.etc.version import iswin
from minghu6.metaclass import metaclass_append_attributes
from minghu6.typing import *


################################################################################
#### Decorators

@contextmanager
def mkstempfile(
    suffix: str | None = None,
    prefix: str | None = None,
    dir: StrPath | None = None,
    text: bool = False
):
    _fd, fpath = tempfile.mkstemp(
        suffix=suffix, prefix=prefix, dir=dir, text=text)

    fpath = Path(fpath)

    try:
        yield fpath
    finally:
        fpath.unlink(missing_ok=True)


@contextmanager
def unlink(
    file: StrPath
):
    file = Path(file)

    try:
        yield file
    finally:
        file.unlink(missing_ok=True)


################################################################################
#### Command Runner

@dataclass
class RunResult:
    out: str
    err: str
    cmd: str
    code: int

    def as_exception(self) -> CalledProcessError:
        return CalledProcessError(
            self.code,
            self.cmd,
            self.out,
            self.err
        )


def wait_run(cmd, shell=True) -> RunResult:
    """
    only can be used in shell (`exec_cmd("ffmpeg -version")`)
    """
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=shell)

    out, err = p.communicate()

    codec = locale.getencoding()

    try:
        out = out.decode(codec, errors="ignore")
        err = err.decode(codec, errors="ignore")
    except UnicodeDecodeError:
        codec = "utf-8"

        out = out.decode(codec, errors="ignore")
        err = err.decode(codec, errors="ignore")

    return RunResult(out, err, cmd, p.returncode)


def poll_run(cmd) -> Generator[str, None, int]:
    """
    mix stdout and stderr
    """

    metaclass = metaclass_append_attributes(isstderr=False)

    class CustomBytes(bytes, metaclass = metaclass):
        pass

    class CustomStr(str, metaclass = metaclass):
        pass

    def _enqueue_output(process, out, queue):
        for line in iter(out.readline, b""):
            # tag line origin: stdout or stderr
            line = CustomBytes(line)

            if out is process.stderr:
                line.isstderr = True

            queue.put(line)

        while True:
            if process.poll() is not None:
                process.terminate()
                break

    if isinstance(cmd, list):
        cmd = " ".join(cmd)

    p = Popen(
        "{cmd} && exit".format(cmd=cmd),
        stdout=PIPE,
        stderr=PIPE,
        shell=True,
    )

    q = Queue()

    t_stdout = Thread(
        target=_enqueue_output,
        name="{cmd} fetch stdout".format(cmd=cmd),
        args=(p, p.stdout, q),
        daemon=True,
    )
    t_stderr = Thread(
        target=_enqueue_output,
        name="{cmd} fetch stderr".format(cmd=cmd),
        args=(p, p.stderr, q),
        daemon=True,
    )

    t_stdout.start()
    t_stderr.start()

    codec = locale.getencoding()

    while p.returncode is None:
        try:
            raw_line = q.get(timeout=0.1)
            isstderr = raw_line.isstderr
            line = CustomStr(raw_line.strip().decode(codec, errors="ignore"))
            line.isstderr = isstderr
        except Empty:
            pass
        else:
            yield line

    return p.returncode


def realtime_run(cmd: list[str] | str, check: bool = True) -> int:
    if isinstance(cmd, list):
        cmd = " ".join(cmd)

    p = Popen(
        "{cmd}".format(cmd=cmd),
        stdout=sys.stdout,
        stderr=sys.stdin,
        shell=True,
    )

    retcode =  p.wait()

    if check and retcode:
        raise CalledProcessError(retcode)


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
        for line in poll_run(cmd):
            if is_first_line:
                is_first_line = False
                logger.info("start `%s`" % cmd)

            logger.debug(line)

        logger.error("found %s exit..." % cmd)


################################################################################
#### Interactive Utils


def askyesno(
    msg: AnyFormattedText = "", default: bool | None = None
) -> bool:

    end_template = Template(
        " Press "
        "<style>$y</style>"
        "/"
        "<style>$n</style>"
        " "
    )

    if default is None:
        end = HTML(end_template.substitute({'y': 'y', 'n': 'n'}))

    elif default:
        end = HTML(end_template.substitute({'y': '<b>Y</b>', 'n': 'n'}))

    else:
        end = HTML(end_template.substitute({'y': 'y', 'n': '<b>N</b>'}))

    bindings = KeyBindings()

    @bindings.add('enter')
    def _(event):
        buffer: Buffer = event.app.current_buffer

        if default is None:
            return
        elif default:
            buffer.insert_text('Y', overwrite=True)
        else:
            buffer.insert_text('N', overwrite=True)

        event.app.exit(default)

    @bindings.add('y')
    def _(event):
        buffer: Buffer = event.app.current_buffer
        buffer.insert_text('Y', overwrite=True)

        event.app.exit(True)

    @bindings.add('n')
    def _(event):
        buffer: Buffer = event.app.current_buffer
        buffer.insert_text('N', overwrite=True)

        event.app.exit(False)

    body_text = to_formatted_text(msg)
    tail_text = to_formatted_text(end)

    text = body_text + tail_text

    return prompt(
        text,
        key_bindings=bindings,
    )


def ask_goon(msg='  press <Enter> to continue, or q to quit') -> bool:
    bindings = KeyBindings()

    @bindings.add('enter')
    def _(event):
        event.app.exit(True)

    @bindings.add('q')
    def _(event):
        event.app.exit(False)

    return prompt(
        key_bindings=bindings,
        bottom_toolbar=msg
    )


def askoverride(fpath: StrPath, default=None) -> bool:
    fpath = Path(fpath)

    if not fpath.exists():
        raise ValueError(f"{fpath} doesn't exist")

    import html

    fpath = html.escape(str(fpath))

    return askyesno(
        HTML(f"File <i>{fpath}</i>"
                f" Already Exists Overreide ?"),
        default=default
    )


################################################################################
#### Etc.

def alarm(timeout):
    if iswin():
        class _Alarm(Thread):
            def __init__(self, timeout):
                Thread.__init__(self)
                self.timeout = timeout
                self.setDaemon(True)

            def run(self):
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
