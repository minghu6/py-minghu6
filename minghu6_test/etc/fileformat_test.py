# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""
import os

from minghu6.etc import fileformat

def filetype_test():
    from minghu6.etc.path import get_cwd_preDir
    gif_file_path = os.path.join(get_cwd_preDir(2),
                                'resources',
                                'minghu6_test',
                                'etc',
                                'captcha.gif')

    ext_name = fileformat.fileformat(gif_file_path).ext_name
    #print(ext_name)
    assert ext_name == 'gif'



if __name__ == '__main__':

    filetype_test()