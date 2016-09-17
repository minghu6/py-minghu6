#! /usr/bin/env python3
# -*- coding:utf-8 -*-
"""
most of content reference the <Programming Python> by Mark Lutz
################################################################################
用命令行和可复用的启动方案启动python程序；（某些部分假定python、python3在你的系统路径中）

使用subprocess模块也行，不过os.popen()在内部调用subprocess这个模块
multiprocessing模块也是一个选择。

Usage:

from minghu6.etc.launchmods import PortableLauncher as Launch

Launch('echo','echo.py')()
#or
#launch=Launch('echo','echo.py')
#launch.announce()
#launch.run()
################################################################################
"""

import sys,os
import subprocess
import minghu6.etc.version as ver

pypath=sys.executable#such as 'E:\\Coding\\Python3.4\\python3.4.exe'
pyfile=''
if ver.ispython2():
    pyfile='python'
elif ver.ispython3():

    if ver.is_strPython3():
        pyfile='python3'
    elif ver.is_strPython():
        pyfile='python'
    else:
        pyfile=pypath


class LaunchMode:
    '''
    在实例中待命，声明标签(print(what=label))并运行命令(run(cmdline))；
    子类按照run（）中的需要格式化命令行；
    命令应以准备运行的。py脚本名开头（不带脚本完整路径）
    '''

    def __init__(self,label,command, **kwargs):
        self.what=label
        self.where=command
        self.kwargs=kwargs

    def __call__(self):
        self.announce(self.what)
        self.run(self.where, **(self.kwargs))


    def announce(self,text):
        print(text)

    def run(self,cmdline, **kwargs):
        assert False,'run must be defined'



class System(LaunchMode):
    '''
    run python script in shell;
    Warning:It will block the caller except use '&' in unix
    '''
    def run(self,cmdline, **kwargs):
        #os.system('%s %s'%(pyfile,cmdline))
        subprocess.call('%s %s'%(pyfile,cmdline), **kwargs)

class Popen(LaunchMode):
    '''
    run shell command in a new process;
    Warning:Tt will block the caller too because of pipe closing too fast
    '''
    def run(self,cmdline, **kwargs):
        #os.popen(pyfile+' '+cmdline)
        self.popen=subprocess.Popen('%s %s'%(pyfile,cmdline),
                                    **kwargs)


class Fork(LaunchMode):
    '''
    run shell commmand in neew process createa explicitly;
    Warning: only can be used in Unix like system(including cygwin)
    '''
    def run(self,cmdline, **kwargs):
        assert hasattr(os,'fork')
        cmdline=cmdline.split()
        self.popen=subprocess.Popen([pyfile,cmdline], **kwargs)


class Start(LaunchMode):
    '''
    be independent on caller;
    Warning:only can be used in Windows:using additional name association
    '''
    def run(self,cmdline, **kwargs):
        assert ver.iswin()

        os.startfile(cmdline, **kwargs)

class StartArgs(LaunchMode):
    '''
    Warning:
        only can be used in Windows:using `start` of windows cmd;
        '\' has no problem.
    '''
    def run(self,cmdline, **kwargs):
        assert ver.iswin()
        #os.system('  '.join(['start',cmdline])) #maybe create new window
        shell=kwargs.get('shell', True)
        from minghu6.algs.dict import remove_key
        kwargs=remove_key(kwargs, 'shell')


        subprocess.call('  '.join(['start',cmdline]), shell=shell, **kwargs)
################################################################################
#Spawn Maybe The most frenquently used method
################################################################################
class Spawn(LaunchMode):
    '''
    create a new process and run python in the process;
    can be used both Windows and Unix
    '''
    def run(self,cmdline, **kwargs):
        if ver.islinux():
            #os.spawnv(os.P_DETACH,pyfile,(pyfile,cmdline))
            self.popen=subprocess.Popen('%s %s'%(pyfile,cmdline), **kwargs)
        elif ver.iswin():
            #os.spawnv(os.P_NOWAIT,pyfile,(pyfile,cmdline))
            self.popen=subprocess.Popen('%s %s'%(pyfile,cmdline), **kwargs)


class Top_Level(LaunchMode):
    '''
    run in a new window ,same process;...need GUI Info
    '''
    def run(self,cmdline, **kwargs):
        assert False,'Sorry - mode not yet implemented'



#
#choose a portable launcher for self platform
#maybe need refinnement later
#

if ver.iswin():
    #PortableLauncher=Spawn
    PortableLauncher=Popen
else:
    PortableLauncher=Fork


class QuietPortableLauncher(PortableLauncher):
    '''
    do nothing excpt redefine the announce doing nothing
    '''
    def announce(self,text):
        pass

def selftest():
    '''
    only for test...
    '''
    file='echo.py'
    os.system('echo print(\'hi\') > %s'%file)
    input('default mode ...')
    PortableLauncher(file,file)()


    input('system mode ...')
    System(file,file)()

    if ver.iswin():
        input('DOS start mode...')
        StartArgs(file,file, shell=True)()

if __name__=='__main__':
    selftest()

