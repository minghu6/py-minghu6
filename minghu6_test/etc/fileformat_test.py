# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""
import os

from minghu6.etc import fileformat

def test_filetype():
    from minghu6.etc.path import get_pre_path
    gif_file_path = os.path.join(get_pre_path(__file__, 3),
                                'resources',
                                'minghu6_test',
                                'etc',
                                'captcha.gif')

    ext_name = fileformat.fileformat(gif_file_path).ext_name
    #print(ext_name)
    assert ext_name == 'gif'



if __name__ == '__main__':

    test_filetype()