# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""

"""

def exist_cmd_test():
    from minghu6.etc.cmd import exec_cmd

    info, err = exec_cmd('python --version')

    assert len(info)!= 0 and len(err)==0

    # assumn that java exists (java is strange and ugly)
    info, err = exec_cmd('java -version')
    assert len(info)== 0 and len(err)!=0


from minghu6.algs.decorator import ignore
# ignore all exception
@ignore
def DoNotHaveProperVersion_test():
    from minghu6.etc.cmd import DoNotHaveProperVersion
    raise DoNotHaveProperVersion('this is DoNotHaveProperVersion')

def has_proper_git_test():
    from minghu6.etc.cmd import has_proper_git

    flag=has_proper_git(min_version_limit='2.8.1')
    print('git min_verlimit < now {0}'.format(flag))


def has_proper_java_test():
    from minghu6.etc.cmd import has_proper_java
    flag=has_proper_java(min_version_limit='1.7.0')
    print('java min_verlimit < now {0}'.format(flag))

def has_proper_tesseract_test():
    from minghu6.etc.cmd import has_proper_tesseract
    flag=has_proper_tesseract(min_version_limit='3.5.0')
    print('tesseract min_verlimit < now {0}'.format(flag))

def has_proper_ffmpeg_test():
    from minghu6.etc.cmd import has_proper_ffmpeg
    assert has_proper_ffmpeg() == True


if __name__ == '__main__':
    exist_cmd_test()
    has_proper_git_test()
    has_proper_java_test()
    has_proper_tesseract_test()
    DoNotHaveProperVersion_test()
    has_proper_ffmpeg_test()
