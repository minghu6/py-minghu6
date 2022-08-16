#! /usr/bin/env python3
# -*- Coding:utf-8 -*-

"""
################################################################################
Install Shell Completions (Only Bash)
################################################################################
"""

import os
import platform
import subprocess

SRC_HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMPLETIONS_DIR = os.path.join(SRC_HOME, 'minghu6', 'tools', 'completions')
DST_DIR = '~/.local/share/bash-completion/completions/'

def cli():
    if not platform.platform().upper().startswith('LINUX'):
        print("Completions just support Linux Bash!")
        return

    print(f'Detect completions dir: {COMPLETIONS_DIR}')
    print(f'Install into: {DST_DIR}')

    for fn in os.listdir(COMPLETIONS_DIR):
        to_fn = fn.split('_completion')[0]
        src = os.path.abspath(os.path.join(COMPLETIONS_DIR, fn))
        print(f'==> {src}')
        dst = os.path.abspath(os.path.join(DST_DIR, to_fn))
        subprocess.check_output(['/usr/bin/ln', '-i', src, dst], shell=False)


if __name__ == '__main__':
    cli()
