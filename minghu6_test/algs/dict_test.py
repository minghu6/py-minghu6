# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""

def test_remove_key():
    from minghu6.algs.dict import remove_key

    d=dict({0:'a',1:None,2:None,3:'d', None:'a', None:None, 'n':5})
    assert {0:'a', 1:None, 2:None, 3:'d', 'n':5} == remove_key(d, None)
    assert {0:'a', 'n':5} == remove_key(d, {1, 2, 3, None,})

    d2={'nn':3,'num': '5',
        'split_method': None,
        'func': '<function main_split at 0x00000233F6143D08>',
        'path': 'D:\\Coding\\Python35\\python_scripts\\Test\\crawl\\1_test.gif',
        'outdir': '.'}

    assert remove_key(d2, 'func') == {'path':'D:\\Coding\\Python35\\python_scripts\\Test\\crawl\\1_test.gif',
                                      'outdir': '.',
                                      'split_method': None,
                                      'nn': 3,
                                      'num': '5'}

if __name__ == '__main__':

    test_remove_key()
