"""leetcode
A leetcode project generator
Usage:
  leetcode new <question_title> <lang>...
  leetcode add <lang>...

Options:
  new                  create a new project.
  <question_title>
  <lang>               language subproject such as py, rs, etc.

"""

import re
from enum import Enum
from typing import List
from os.path import dirname, join, basename

from docopt import docopt
from sh import mkdir, cd, cp, pwd, cargo
from schema import Schema, SchemaError, Regex, And, Optional, Or

from minghu6 import __version__, TEMPLATES_HOME


HOME = join(TEMPLATES_HOME, 'leetcode')
HOME_PY = join(HOME, 'py')
HOME_RS = join(HOME, 'rs')

PAT_QUESTION_TITLE = re.compile('^(\d{4})_[0-9a-z_]+$')
LANG_IDTS = ['py', 'rs']


class Lang(Enum):
    Python = 'py'
    Rust = 'rs'

prev_dir = lambda: dirname(str(pwd()))
cd_previous = lambda: cd(prev_dir())


def create_lang_subfolder_py(question_id: str):
    mkdir(['-p', f'py{question_id}'])
    cd(f'py{question_id}')

    cp([join(HOME_PY, '0.py'), '.'])
    cp([join(HOME_PY, '.bandit'), '.'])

    cd_previous()


def create_lang_subfolder_rs(question_id: str):
    cargo([
        'generate',
        '--git',
        'https://github.com/minghu6/crate-templates.git',
        'leetcode',
        '--lib',
        '--name',
        f'rs{question_id}'
    ], _tty_out=False)


def create_proj(question_title: str, langs: List[Lang]):
    m = re.match(PAT_QUESTION_TITLE, question_title)
    question_id = m.group(1)

    mkdir(['-p', question_title])
    cd(question_title)

    for lang in langs:
        globals()[f'create_lang_subfolder_{lang.value}'](question_id)

    cd_previous()


def add_subfolder(question_id: str, langs: List[Lang]):
    for lang in langs:
        globals()[f'create_lang_subfolder_{lang.value}'](question_id)


def cli():
    arguments = docopt(__doc__, version=__version__)

    schema = Schema({
        Optional('new'): Or(True, False),
        Optional('add'): Or(True, False),
        '<question_title>': Or(Regex(PAT_QUESTION_TITLE), None),
        '<lang>': [And(
            lambda x: x in LANG_IDTS,
            error=f'<LANG> should be either of {LANG_IDTS}')]
    })

    try:
        arguments = schema.validate(arguments)
    except SchemaError as e:
        exit(e)

    if arguments['<lang>']:
        langs = [Lang(lang) for lang in arguments['<lang>']]


    if arguments['new']:
        create_proj(arguments['<question_title>'], langs)
    elif arguments['add']:
        question_title = basename(str(pwd()))

        m = re.match(PAT_QUESTION_TITLE, question_title)

        if m is None:
            exit(f'Invalid parent name: {PAT_QUESTION_TITLE} for {question_title}')

        add_subfolder(m.group(1), langs)


if __name__ == '__main__':
    cli()
