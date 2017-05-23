# -*- coding:utf-8 -*-
# !/usr/bin/env python3

"""

"""

from minghu6.algs.decorator import ignore


# ignore all exception
@ignore
def DoNotHaveProperVersion_test():
    from minghu6.etc.cmd import DoNotHaveProperVersion
    raise DoNotHaveProperVersion('this is DoNotHaveProperVersion')


def has_proper_git_test():
    from minghu6.etc.cmd import has_proper_git
    flag = has_proper_git()
    assert flag


def has_proper_java_test():
    from minghu6.etc.cmd import has_proper_java

    flag = has_proper_java(min_version='1.7.0')
    assert flag


def has_proper_tesseract_test():
    from minghu6.etc.cmd import has_proper_tesseract
    flag = has_proper_tesseract()
    assert flag


def has_proper_ffmpeg_test():
    from minghu6.etc.cmd import has_proper_ffmpeg
    assert has_proper_ffmpeg() == True


def test_has_proper_chromedriver():
    from minghu6.etc.cmd import has_proper_chromedriver
    has_proper_chromedriver()


def test_has_proper_geckodriver():
    from minghu6.etc.cmd import has_proper_geckodriver
    has_proper_geckodriver()


if __name__ == '__main__':
    has_proper_git_test()
    has_proper_java_test()
    has_proper_tesseract_test()
    DoNotHaveProperVersion_test()
    has_proper_ffmpeg_test()
    test_has_proper_chromedriver()
    test_has_proper_geckodriver()
