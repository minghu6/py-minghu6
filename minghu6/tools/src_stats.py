from genericpath import isdir
from os import curdir
from sh import wc
from os.path import curdir, abspath
from pathlib import Path

from minghu6.tools.lc import count_lines_dir

source_dir = Path(curdir())

ext_filter = [".c", ".h"]
stats = []

for sub in source_dir.iterdir():
    if sub.isdir():
        wc('.', '-l', )