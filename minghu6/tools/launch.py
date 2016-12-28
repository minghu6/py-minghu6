#!/usr/bin/env python3
#-*- coding:utf-8 -*-
#python 3


"""

A very Beautiful Launcher for Clojure Launching
and Java Program easy configure and quick starting.

In my mind, xml tools like Ant is designed for program but for humanbeings
xxmake is too old that makes it a burden.Mavn ,what is it?!.
Lein May be o good idea,but I don't know why it need proxy ?!.
And because of our greate the GREATE WALL,i can't connect using lein.

En,that's the reason why I create a saming wheel...
It's useful indeed,however.

bpython is different ipython

"""
import configparser
import os
import platform
import shelve
import sys
from argparse import ArgumentParser

import minghu6.etc.version as myos
import minghu6.tools.find_max as search
import minghu6.text.SequenceEnhance as seh
from minghu6.algs import const


const.CLOJURE_JAR='^.*clojure.*.jar$'
const.DBNAME=os.path.join(os.path.expanduser('~'),'.mydb')
const.CLOJURE='clojure'


const.COMPILE='compile'
const.RUN='run'

const.JAVA='java'
const.JAVA_CP='cp'
const.JAVA_D='d'
const.JAVA_TARGET='target'
const.JAVA_MAIN='main'

const.PYTHON_MAIN='main'
const.PYTHON='python'
const.PYTHON_VERSION='version'# python2|python3
const.PYTHON_SUB_VERSION='sub_version' #optional not be implemented...
const.PYTHON_SRC='src'#absolute path like src=%(src_dir)s/xxx.py
const.PYTHON_SRC_DIR='src_dir'
const.PYTHON2='python2'
const.PYTHON3='python3'



const.CONFIG_PATH='config_path'
const.CONFIG_DESC='config_desc'
const.CONFIG_DEFAULT='default' # config_desc: describe the ini file content
const.CONFIG_ALIAS='alias'


class NothingSelectException(Exception):pass


def shell_interactive():
    parser=ArgumentParser()
    
    parser.add_argument('--repl',dest='clojure_repl_flag',action='store_true',
                        help='start clojure repl')
    
    parser.add_argument('iteral',metavar='other_args',nargs='*',
                        help='Nore: use -- to pass the args start with -/-- ')

    parser.add_argument('--config_file',
                        help='point to the config file path ')
    parser.add_argument('--alias',
                       help='point to the config file\'s alias')

    parser.add_argument('--use',
                       help='use alias of config_file')

    parser.add_argument('-c','--compile',dest='__compile',action='store_true',
                       help='compile thr progeam use alias config')

    parser.add_argument('-m','--main',
                        help='point to the main func manualy for run program')

    parser.add_argument('-l','--list',dest='view_files',metavar='alias_names',
                        nargs='+',
                        help='list the config file accoding to alias,'
                        '* for all')

    parser.add_argument('-sl','--shortlist',action='store_true',
                        help='short list all the ini file name')

                        
    parser.add_argument('--update',dest='update_files',metavar='alias_names',
                        nargs='+',
                        help='update the config file accoding to alias,'
                        '* for all')
    #rm!! care!!
    parser.add_argument('-rm','--remove',dest='remove_files',
                        metavar='alias_names',
                        nargs='+',
                        help='rm the record (do not rm the physical file)')

    
    parser.add_argument('--refind',dest='refind_list',metavar='[clojure|python|*]',
                        nargs='+',
                        help='refind some confirm config such as clojure jar')
        
    args=parser.parse_args()

    #print(args.iteral)
    
    if args.clojure_repl_flag:
        args.__dict__['run_clojure_flag']=False
        
    from minghu6.algs.dict import remove_value
    return remove_value(args.__dict__,None)


def selector(iteral,run_clojure_flag=True,
             clojure_repl_flag=False,
             config_file=None,
             alias=None,
             use=None,
             __compile=False,
             main=list(),
             view_files=None,
             shortlist=False,
             update_files=None,
             remove_files=None,
             refind_list=None):
    """
    select the correct launcher
    """

    db=shelve.open(const.DBNAME)

    cmd=''
    if clojure_repl_flag: #run clojure repl
        cmd=clojure_repl(iteral,db)
        
        
    elif config_file !=None: #commit config file
        cmd=config_file_read(config_file,alias,db)

    elif use !=None:
        cmd=config_file_use(use,iteral,__compile,main,db)

    elif view_files!=None:
        cmd=config_file_view(view_files,db)

    elif shortlist !=False:
        cmd=config_file_quick_view(db)
        
    elif update_files!=None:
        cmd=config_file_update(update_files,db)

    elif remove_files!=None:
        cmd=config_file_remove(remove_files,db)
    elif refind_list!=None:
        cmd=refind(refind_list,db) 
        
    elif run_clojure_flag:#run clojure sciptes
        cmd=run_clojure(iteral,db)
        
    else:
        db.close()
        raise(NothingSelectException)

    db.close()
    return cmd
################################################################################
"""
language mode
"""
    
def java_mode(alias,iteral,__compile,main,db):
    """
    reference const defination
    """
    dic=db[alias]
    
    config_dic={}
    
    java_str=''
    cp_str=''
    d_str=''
    
    target_str=''
    main_str=''
    
    spc=''
    if myos.iswin():
        spc=';'
    elif myos.islinux():
        spc=':'

        
    if myos.iswin():
        if __compile:
            config_dic=dic[const.COMPILE]
            if const.JAVA_D in config_dic:
                d_str=config_dic[const.JAVA_D]
                java_str=' '.join(['javac','-d '+d_str])
                
            if const.JAVA_CP in config_dic:
                cp_str=config_dic[const.JAVA_CP]
                java_str=' '.join([java_str,'-cp '+cp_str])
                
            if const.JAVA_TARGET in config_dic:
                '''
                consider of more than one target
                '''   
                target_str=config_dic[const.JAVA_TARGET]
                targets=seh.parseStr(target_str.split(spc))

                assert (len(targets)!=0)
                
                tmp_str=''
                link='&&'
                for target in targets:
                    tmp_str+='  '.join([java_str,target])
                    tmp_str+=link
                    #print('??????')
                
                java_str=tmp_str[:-len(link)]
                
        else:# run
            config_dic=dic[const.RUN]

            if const.JAVA_CP in config_dic:
                cp_str=config_dic[const.JAVA_CP]
                java_str=' '.join(['java','-cp '+cp_str])
                
            if const.JAVA_MAIN in config_dic:
                if main==list():
                    main_str=config_dic[const.JAVA_MAIN]
                else:
                    main_str=main
                    
                java_str=' '.join([java_str,main_str])
                
    elif myos.islinux():    
        raise Exception('UnImplemented')

    #print(iteral)
    for item in iteral:
        java_str=' '.join([java_str,item])

    return java_str


def python_mode(alias,iteral,__compile,main,db):
    """
    reference const defination
    """
    dic=db[alias]
    
    def confirm_python_version(dic):
        ver=dic[const.PYTHON][const.PYTHON_VERSION]
        if ver==const.PYTHON2:
            ver='python'
        elif ver==const.PYTHON3:
            ver='python3'
            if os.system('python3 -c __import__(\'os\')')==1:#error
                '''
                use this python3 version
                '''
                ver=platform.python_version()
                ver=ver.split('.')
                ver=ver[0]+'.'+ver[1]

        return ver

    py_ver=confirm_python_version(dic)
    config_dic=[]
    
    if __compile:
        pass

    else:#run
        config_dic=dic[const.RUN]
        src_dir=config_dic[const.PYTHON_SRC_DIR]
        cmd0=' '.join(['cd',src_dir])#cd to python file current vdir
        
        src=config_dic[const.PYTHON_SRC]
        src_dir=config_dic[const.PYTHON_SRC_DIR]
        
        for item in iteral:
            src=' '.join([src,item])


        #test if exist specific target to run
        if main==list():
            target=src
            
        else:
            main_str=main
            
                        
            target=os.path.join(src_dir,main_str)
            #print('*******\n',main_str,'*********\n')
        cmd=' '.join([py_ver,target])
        
        
        if os.system(' && '.join([cmd0,cmd]))==1:#error code is 1
            for p in python_find(db):

                cmd=' '.join([p,target])
                if os.system(' && '.join([cmd0,cmd]))==0:
                    break
        print(' && '.join([cmd0,cmd]))
        
    return ''


    
#################################################################################
def config_file_use(alias,iteral,__compile,main,db):
    """
    use config file
    """
 
    
    dic=db[alias]
    cmd=''
    if const.JAVA in dic:
        cmd=java_mode(alias,iteral,__compile,main,db)

    elif const.PYTHON in dic:
        cmd=python_mode(alias,iteral,__compile,main,db)

    
    return cmd

def regular_formular(files,db):
    """
    regular formular,side-effect
    """
    if '*' in files:
        files.clear()

        #print('Error',files)
        
        [files.append(item[const.CONFIG_DEFAULT][const.CONFIG_ALIAS])
         for item in db.values() if isinstance(item,configparser.ConfigParser)]

def refind(refind_list,db):
    """
    research the confirm config
    """
    su_token=False
    
    if '*' in refind_list:
        su_token=True

    if const.PYTHON in refind_list or su_token:
        py_ver=__python_find()
        db[const.PYTHON]=py_ver

    if const.CLOJURE in refind_list or su_token:
        clojure=__clojure_find()
        db[const.CLOJURE]=clojure

    return ''

def config_file_update(update_files,db):
    
    regular_formular(update_files,db)

    
    
    [config_file_read(db[alias][const.CONFIG_DEFAULT][const.CONFIG_PATH],alias,db)
     for alias in update_files]
    

    
    return ''


def config_file_remove(remove_files,db):

    
    for item in remove_files:
        if isinstance(db[item],configparser.ConfigParser):
            db.pop(item)
        else:
            raise Exception(item,'is not valid alias name')

    return ''
    
def config_file_view(view_files,db):
    """
    view the config files
    """
    
        
    regular_formular(view_files,db)
    
    [config_template_print(alias,db) for alias in view_files]
    

    return ''


def config_file_quick_view(db):
    """
    quick view all the config file
    """

    [print(item)
         for item in db.keys() if isinstance(db[item],
                                             configparser.ConfigParser)]

    return ''
    
def config_template_print(alias_name,db):
    """
    view the single config file,called by config_file_view
    """    
    if alias_name in db:
        alias_config=db[alias_name]
        print('*'*80)
        print()
        print('Alias:{0:s}'.format(alias_name))
        print('Config Path:{0:s}'.format(alias_config
                                         [const.CONFIG_DEFAULT][const.CONFIG_PATH]))
            
        print('Description:{0:s}'.format(alias_config
                                         [const.CONFIG_DEFAULT][const.CONFIG_DESC]))
        print('')
        print('*'*80)
        for p in alias_config:
            if p not in {const.CONFIG_DEFAULT}:
                print('[{0:s}]'.format(p))
                [[print(pp,'\n',alias_config[p][pp])]for pp in alias_config[p]]
                print('\n')

        print('\n\n')
                
def config_file_read(config_file,alias,db):
    """
    read config file
    """
        
    if alias==None:
        alias=config_file
        
    if myos.iswin() or myos.islinux():
        config=configparser.ConfigParser()
        config.read(config_file)
        with open(config_file) as f:
            name=f.name

        desc='Nothing'
        if (const.CONFIG_DEFAULT in config and
            const.CONFIG_DESC in config[const.CONFIG_DEFAULT]):
            
            desc=config[const.CONFIG_DEFAULT][const.CONFIG_DESC]
        
        config[const.CONFIG_DEFAULT]={const.CONFIG_PATH:name,
                                      const.CONFIG_ALIAS:alias,
                                      const.CONFIG_DESC:desc}

        
    db[alias]=config


    return ''

def __python_find():
    """
    Dynamic find the python form can be used
    python
    python3
    python3.1-python3.7
    """
    py_ver=list()
    
    py='python'
    if os.system(py+' --version')==0:#return 0 for ok,1 for error(confusing)
        py_ver.append(py)
        
    py3='python3'
    if os.system(py3+' --version')==0:
        py_ver.append(py3)
    for i in range(7):
        one=py3+'.'+str(i+1)
        if os.system(one+' --version')==0:
            py_ver.append(one)

    return py_ver   
           
def __clojure_find():
    """
    Dynamic find the matched clojure.jar
    """
    spc=''
    if myos.iswin():
        spc=';'
    elif myos.islinux():
        spc=':'

    p=''
    if 'classpath' in os.environ:
        p=os.environ['classpath'].split(spc)
    elif 'CLASSPATH' in os.environ:
        p=os.environ['CLASSPATH'].split(spc)

    p=seh.parseStr(p)
    file=[]
    for path in p:
        result=search.file_search(dirname=path,
                                    inner=True,
                                    pattern=const.CLOJURE_JAR)[0]         
        if  result!=[]:
             [file.append(item) for item in result]

                
    return file


def python_find(db):
    """
    Lazy  find using __clojure_find and shelve
    """
    python_ver=list()
    if const.PYTHON  in db:
        python_ver=db[const.PYTHON]
    else:
        python_ver=__python_find()
        db[const.PYTHON]=python_ver

    return python_ver


def clojure_find(db):
    """
    Lazy  find using __clojure_find and shelve
    """
    str_clojure=''
    if myos.iswin() or myos.islinux():
        
        
        file=[]
        valid_file=[]
        if const.CLOJURE in db:
            file=db[const.CLOJURE]
            for item in file:
                if os.path.exists(item):
                    valid_file.append(item) 
                        
        if len(valid_file) == 0:
            valid_file=__clojure_find()
            db[const.CLOJURE]=valid_file

                
        str_clojure=valid_file[0]
        db.close()
    return str_clojure
        
        
def clojure_repl(iteral,db):
    """
    run clojure repl
    """
    str_clojure='java -cp '+clojure_find(db)+' clojure.main'

    return str_clojure


def run_clojure(iteral,db):
    """
    run the clojure script
    """

    str_clojure='java -jar '+clojure_find(db)
        
    for arg in iteral:
        str_clojure=' '.join([str_clojure,arg])
        
    return str_clojure

def interactive():
    li=shell_interactive()
    sys.argv.remove(sys.argv[0])

    cmd=selector(**li)

    print(cmd)
    os.system(cmd)


if __name__=='__main__':

    interactive()
    #os.system('pause')
