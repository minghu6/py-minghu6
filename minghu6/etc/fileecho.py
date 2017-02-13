# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""
import _io
from collections import deque
import os
import cchardet as chardet

__all__ = ['head', 'tail', 'guess_charset']

def head(fp:[_io.BufferedReader, _io.FileIO], n=5):
    old_seek= fp.tell()
    result_to_echo = [line for i, line in enumerate(fp) if i<n]
    fp.seek(old_seek, os.SEEK_SET)
    return result_to_echo

def tail(fp:[_io.BufferedReader, _io.FileIO], n=5):

    if 'rb' in fp.mode:
        lf_char = b'\n'
    else:
        lf_char = '\n'

    blk_size_max = 4096 # mutable var
                        # (double util ge than cur_pos, if no lf_char found)
    n_lines = deque()
    old_seek = fp.tell() # save to return

    fp.seek(0, os.SEEK_END)
    cur_pos = fp.tell()

    while cur_pos > 0 and len(n_lines) < n:

        blk_size = min(blk_size_max, cur_pos) # short file

        fp.seek(cur_pos - blk_size, os.SEEK_SET)
        blk_data = fp.read(blk_size)
        lines = blk_data.split(lf_char)

        # have reached the file head
        if len(lines) == 1 and blk_size < blk_size_max:
            n_lines.insert(0, lines[0])
            break

        # no lf_char in buff
        elif len(lines) == 1 and blk_size == blk_size_max and blk_size < cur_pos:
            blk_size_max *= 2

        # no if_char in the whole file
        elif len(lines) == 1 and blk_size == blk_size_max and blk_size >= cur_pos:
            n_lines.insert(0, lines[0])
            break

        else:
            [n_lines.insert(i, line) for i, line in enumerate(lines[1:])]
            cur_pos -= (blk_size - len(lines[0]))

    fp.seek(old_seek, os.SEEK_SET) #reload old_seek

    return list(n_lines)[-n:]

def guess_charset(fp:[_io.BufferedReader, _io.FileIO]):
    if 'b' in fp.mode:
        cr = b'\n'
    else:
        cr = '\n'

    res_list = head(fp, 100)
    res = cr.join(res_list)
    if 'b' not in fp.mode:
        res = res.encode(fp.encoding)
    detect_head_result = chardet.detect(res)

    res_list = tail(fp, 100)
    res = cr.join(res_list)
    if 'b' not in fp.mode:
        res = res.encode(fp.encoding)

    detect_tail_result = chardet.detect(res)
    if detect_head_result['encoding'] != detect_tail_result['encoding']:
        return None, None # means unknown
    else:
        return detect_tail_result['encoding'], detect_tail_result['confidence']
