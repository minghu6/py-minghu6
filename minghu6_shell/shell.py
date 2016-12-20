# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""
import sys
import shlex
import getpass
import socket
import signal

from minghu6_shell.func import *
from minghu6_shell.func.constants import *

from minghu6.etc.version import iswin
from minghu6.etc.cmd import exec_cmd
from minghu6.text.color import color

built_in_cmds = {}

def tokenize(string):
    """
    # parse the command
    # 比如，'ls -l /home/shiyanlou' 划分之后就是
    # ['ls', '-l', '/home/shiyanlou']
    :param string:
    :return:
    """
    return shlex.split(string)

def preprocess(tokens):
    processed_token = []
    for token in tokens:
        if token.startswith('$'):
            processed_token.append(os.getenv(token[1:]))
        else:
            processed_token.append(token)

    return processed_token

def handler_kill(signum, frame):
    raise OSError("Killed!")

def execute(cmd_tokens):
    with open(HISTORY_PATH, 'a') as history_files:
        history_files.write(' '.join(cmd_tokens) + os.linesep)

    if cmd_tokens:
        cmd_name = cmd_tokens[0]
        cmd_args = cmd_tokens[1:]
        if cmd_name in built_in_cmds:
            return built_in_cmds[cmd_name](cmd_args)

        signal.signal(signal.SIGINT, handler_kill)
        exec_cmd(' '.join(cmd_tokens))

    return SHELL_STATUS_RUN

def display_cmd_prompt():
    user = getpass.getuser()
    hostname = socket.gethostname()
    cwd = os.getcwd()
    base_dir = os.path.basename(cwd)
    home_dir = os.path.expanduser('~')
    if cwd == home_dir:
        base_dir = '~'


    color.print_info('({0}:{1}){2}$'.format(user,
                                            hostname,
                                            base_dir), end='')

    sys.stdout.flush()

def ignore_signals():
    if not iswin():
        signal.signal(signal.SIGTSTP, signal.SIG_IGN)

    signal.signal(signal.SIGINT, signal.SIG_IGN)


def shell_loop():
    status = SHELL_STATUS_RUN
    while status == SHELL_STATUS_RUN:
        display_cmd_prompt()
        ignore_signals()
        try:
            cmd = sys.stdin.readline()
            cmd_tokens = tokenize(cmd)
            cmd_tokens = preprocess(cmd_tokens)
            status = execute(cmd_tokens)
        except:
            _, err, _ = sys.exc_info()
            color.print_err(err)


def register_command(name, func):
    """
    register command
    :param name:
    :param func:
    :return:
    """
    built_in_cmds[name] = func


def init():
    """
    register all command
    :return:
    """
    register_command('cd', cd)
    register_command('exit', exit)
    register_command('getenv', getenv)
    register_command('history', history)

def main():
    init()
    shell_loop()

if __name__ == '__main__':

    main()


