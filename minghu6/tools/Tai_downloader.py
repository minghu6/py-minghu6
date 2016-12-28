# -*- coding: utf-8 -*-
#! /usr/bin/env python
from __future__ import  print_function #both for py2 and py3,must at top of file

"""
YinYueTai MV download Tool
First Author: Tsing in zhihu https://www.zhihu.com/people/wq123
Modified by minghu6
"""
import sys
import os
import re
def python_version():return sys.version_info.major


if python_version()==3:
    from urllib.request import Request #python3
    from urllib.request import urlopen #python3

    from urllib.request import urlretrieve #python3

    from html.parser import HTMLParser
elif python_version()==2:
    from urllib2 import Request
    from urllib2 import urlopen

    from urllib import urlretrieve

    from HTMLParser import HTMLParser

plus = '█'
def get_progress_bar(now_size, total_size, max_length=25,extra_str=''):
    """

    :param now_size:
    :param total_size:
    :param max_length:
    :return:
    """
    now_length = int(now_size * max_length / total_size)
    
    progress='|-'+plus*now_length+(max_length-now_length)*2*' '+'-|'+extra_str
    progress+=' ' # to avoid repeating last non-blank char in progress in shell 


    progress_bar = progress

    return progress_bar


def report(count, block_size, total_size):

    download_size=count * block_size
    percent = (download_size * 100 / total_size)
    if percent >= 100:
        percent = 100

    pts=('\rdownload ...'
         '\t{0:.3f} mb ').format(download_size / 10e5)
    pts2=get_progress_bar(download_size, total_size,
                          extra_str='{0:.2f}%'.format(percent))

    pts=''.join([pts, pts2])
    sys.stdout.flush()
    if iswin():


        with printDarkSkyBlue():
            print(pts,end='',flush=True)

    elif islinux():
        print(UseStyle(pts,'cyan'),end='',flush=True)

    else:
        print(pts,end='',flush=True)



MV_NOT_EXIST='mv  not  exist'

def get_mv_name(mv_id):

    #get html according to mv_id
    def get_correct_urlobj(mv_id):
        urls=['http://v.yinyuetai.com/video/'+str(mv_id),
              'http://v.yinyuetai.com/h5/video/'+str(mv_id)]

        for url in urls:
            try:
                i=urlopen(url)
            except Exception as ex:
                pass
            else:
                return i

    i=get_correct_urlobj(mv_id)
    html=i.read()

    if python_version()==3:
        codec = i.info().get_param('charset', 'utf8')
        html = html.decode(codec, errors='ignore')

    i.close()

    #parse html and get title

    class Hpr(HTMLParser):


        def handle_starttag(self,tag,attr):
            if tag=='title':
                self.handle_data=self.get_data
                self.data=list()

        def handle_endtag(self,tag):
            if tag=='title':
                self.handle_data=self.do_nothing


        def do_nothing(self,data):
            pass
        def get_data(self,data):

            self.data.append(data)

    if python_version()==3:
        hpr=Hpr(convert_charrefs=False)
        hpr.feed(html)
    elif python_version()==2:
        hpr=Hpr()
        hpr.feed(unicode(html,'utf-8'))

    mv_name=''.join(hpr.data)
    hpr.close()
    def format_mv_name(mv_name):
        #because of MPEG-4 belongs to MP4
        if python_version()==2:
            "bytes"
            mv_name=mv_name.encode('utf-8')

        #mv_name_formatted=mv_name.split('\n\t')[-1].split('-')[1]+'--音悦Tai'+'.mp4'
        pat=r'(?<=-).*(?=-高清MV)'
        m=re.search(pat,mv_name)
        mv_name_formatted=m.group(0)+'--音悦Tai'+'.mp4'


        #mv_name_formatted=mv_name.split('\n\t-')[1].split('高清MV')[0]+'-音悦Tai'+'.mp4'

        return mv_name_formatted

    def filter_invalid_char(basefn,invalid_set={'\\','/','*','?','"','<','>','|'}):
        return ''.join((list(filter(lambda x:x not in invalid_set,basefn))))


    return filter_invalid_char(format_mv_name(mv_name))



def askyesno(prompt='',end='(y/n)',default=None):
    if sys.version_info.major==2:
        global input
        input=raw_input
    #sys.stdout.flush()
    if iswin():
        with printDarkRed():
            value=input(prompt+end).strip().upper()
    elif islinux():
        value=input(UseStyle(prompt+end, 'red')).strip().upper()
    else:
        value=input(prompt+end).strip().upper()

    if value in  ('Y','YES') or (value=='' and default==True):
        return True
    elif value in ('N','NO') or (value=='' and default==False):
        return False
    else :
        return askyesno(prompt=prompt,end=end,default=default)

RESOLUTION_TOO_LOW='resolution_too_low'
error_dict=dict()
def main(mv_id,output_dir='',resolution='720p',tourl=None):

    resolution_map={'240p':0,'480p':1,'720p':2,'1080p':3}
    minimum=resolution_map[resolution]

    mv_id=str(mv_id)

    url='http://www.yinyuetai.com/insite/get-video-info?flex=true&videoId='+mv_id
    timeout=30

    headers={'User-Agent':('Mozilla/5.0(Windows NT 6.3)'
                           'AppleWebKit/537.36 (KHTML,like Gecko)'
                           'Chrome/39.0.2171.95'
                           'Safari/537.36'),
             'Accept':('text/html,application/xhtml+xml,'
                       'application/xml;'
                       'q=0.9,image/webp,*/*;q=0.8')}

    req=Request(url,None,headers)

    if python_version()==3:
        with urlopen(req,None,timeout) as res:
            html=res.read()
            codec = res.info().get_param('charset', 'utf8')
            html = html.decode(codec,errors='ignore')

    elif python_version()==2:
        res=urlopen(req,None,timeout)
        html=res.read()


    reg=r'http://\w*?\.yinyuetai\.com/uploads/videos/common.*?(?=&br)'
    pattern=re.compile(reg)
    findList=re.findall(pattern, html) #find all version of MV

    if len(findList)==0:
        error_dict[mv_id]=MV_NOT_EXIST
        if iswin():
            with printDarkRed():
                print(MV_NOT_EXIST)
        elif islinux():
            print(UseStyle(MV_NOT_EXIST,'red'))
        else:
            print(MV_NOT_EXIST)
        return

    if len(findList)>=minimum+1:
        #print(findList)
        mvurl=findList[-1] # :240p 0 :480p 1 :720p 2 :1080p 3
    else:
        if iswin():
            with printDarkRed():
                print(RESOLUTION_TOO_LOW)
        elif islinux():
            print(UseStyle(RESOLUTION_TOO_LOW,'red'))
        else:
            print(RESOLUTION_TOO_LOW)

        return

    filename=get_mv_name(mv_id)
    if filename==MV_NOT_EXIST:
        error_dict[mv_id]=MV_NOT_EXIST
        if iswin():
            with printDarkRed():
                print(MV_NOT_EXIST)
        elif islinux():
            print(UseStyle(MV_NOT_EXIST,'red'))
        else:
            print(MV_NOT_EXIST)
        return
    elif tourl!=None:
        if tourl == 'stdout':
            f = sys.stdout
        else:
            f = open(tourl,'a')

        #with import print_function,so python2 can run it too.
        print('#'+mv_id,file=f)
        print('#'+filename,file=f)
        print(mvurl,file=f)
        print(file=f)
        print(file=f)

        if f != sys.stdout:
            f.close()

        return

    import traceback

    try:

        #some shell codec like Cinese Simplied Windows's gbk
        #    can not decode some unicode character
        ps=':) downloading %s \t'
        try:
            fn_prtable=filename
            if iswin():
                with printDarkSkyBlue():
                    print (ps%fn_prtable)
            elif islinux():
                print(UseStyle(ps%fn_prtable,'cyan'))

            else:
                print (ps%fn_prtable)

        except UnicodeEncodeError:
            fn_prtable=filename.encode('utf-8')
            if iswin():
                with printDarkSkyBlue():
                    print (ps%fn_prtable)
            elif islinux():
                print(UseStyle(ps%fn_prtable,'cyan'))
            else:
                print (ps%fn_prtable)

        try:
            if python_version()==2:
                filename=unicode(filename,'utf-8')

            fullfn=os.path.join(output_dir,filename)

            if os.path.exists(fullfn) and \
                    not askyesno('find Same name file,Overload?'):
                    error_dict[mv_id]=fn_prtable

            else:
                ################################################################
                #DownLoad !!#

                urlretrieve(url=mvurl,
                            filename=fullfn,
                            reporthook=report)

                ################################################################
        except Exception as ex:
            error_dict[mv_id]=MV_NOT_EXIST
            #print(MV_NOT_EXIST)
            if iswin():
                with printDarkRed():
                    traceback.print_exc()
            else:
                traceback.print_exc()
    except Exception as ex:

        pts='\n:( Sorry! The action is failed.\n'
        if iswin():
            with printDarkRed():
                traceback.print_exc()
                print (pts)
        elif islinux():
            traceback.print_exc()
            print(UseStyle(pts,'red'))
        else:
            traceback.print_exc()
            print (pts)
        error_dict[mv_id]=fn_prtable




def mains(mv_ids=set(),filename=None,output_dir='',resolution='720p',tourl=None):
    #print('hi',filename)
    mv_ids=set(mv_ids)
    if filename!=None:

        import os
        try:
            def format_csv(csv_reader):
                iset=set()
                [[iset.add(item.strip()) for item in items if item.strip()!=''] \
                 for items in csv_reader]

                return iset

            import csv
            with open(filename) as f:
                r=csv.reader(f)
                mv_ids=format_csv(r)

        except Exception as ex:
            if iswin():
                with printDarkRed():
                    print(ex)
            elif islinux():
                print(UseStyle(ex.__doc__,'red'))
            else:
                print(ex)
                


    for (i,mv_id) in enumerate(mv_ids):
        if tourl==None:
            pts='\nDownloading ({0:d}/{1:d}) file'.format(i+1,len(mv_ids))
        else:
            pts='\nGeting ({0:d}/{1:d}) urls '.format(i+1,len(mv_ids))
        if iswin():
            with printDarkSkyBlue():
                print(pts)

        elif islinux():
            print(UseStyle(pts,'cyan'))
        else:
            print(pts)

        try:
            main(mv_id,output_dir,resolution,tourl)
        except Exception as ex:
            if iswin():
                with printDarkRed():
                    print(ex)

            elif islinux():
                print(UseStyle(ex,'red'))
            else:
                print(ex)

        print()

    if len(error_dict)==0:

        if tourl==None:
            pts='\n\nDownload complete.'
        else:
            pts='\nGet url complete'
        if iswin():
            with printDarkGreen():
                print(pts)
        elif islinux():
            print(UseStyle(pts,'green'))
        else:
            print(pts)
    else:
        total_num=len(mv_ids)
        failed_num=len(error_dict)
        print('\n\n')

        pts1='total: \t\t%d'%total_num
        pts2='succeed:\t%d'%(total_num-failed_num)
        pts3='failed:\t\t%d'%failed_num
        if iswin():

            with printDarkSkyBlue():
                print(pts1)
            with printDarkGreen():
                print(pts2)
            with printDarkRed():
                print(pts3)

        elif islinux():
            print(UseStyle(pts1,'cyan'))
            print(UseStyle(pts2,'green'))
            print(UseStyle(pts3,'red'))

        else:
            print(pts1)
            print(pts2)
            print(pts3)

        print()

        for key in error_dict:
            pts='{0} : {1} failed\t'.format(key,error_dict[key])
            if iswin():
                with printDarkRed():
                    print(pts)

            elif islinux():
                print(UseStyle(pts,'red'))
            else:
                print(pts)


def interactive():
    from argparse import ArgumentParser

    parser=ArgumentParser()

    parser.add_argument('-f','--file', dest='filename',
                        help=('pass masses of mv id in form of csv file\n'
                              '(can not use with mv_ids at the same time)\n'
                              'ascii comm!! for python2'))

    parser.add_argument('mv_ids', nargs='*',
                        help='pass mv ids(can not use with -f at the same time)')

    parser.add_argument('-o','--output_dir',
                        help='output mv directory')

    parser.add_argument('-r','--resolution', default='720p',
                        choices=['240p','480p','720p','1080p'],
                        help='the minimum resolution you can accept (default 720p)')

    parser.add_argument('-t', '--tourl',
                        help='point a file to save the url (stdout to print)')




    args=parser.parse_args().__dict__
    #print(args)

    if args['output_dir']!=None:
        args['output_dir']=os.path.abspath(args['output_dir'])
        if not os.path.isdir(os.path.abspath(args['output_dir'])):
            raise Exception('arg: -o/--output_dir is not a valid directory')
    else:
        args['output_dir']=''
    if args['filename']==None and args['mv_ids'].__len__()==0:
        raise Exception('too few args need -f or mv_ids')


    #return args

    mains(**args)


################################################################################
# CMD Color Mode
################################################################################
import platform
import ctypes
import sys

def iswin():
    return platform.platform().upper().startswith('WIN')

def islinux():
    return platform.platform().upper().startswith('LINUX')

if iswin():

    STD_OUTPUT_HANDLE = -11
    std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

    def set_cmd_text_color(color, handle=std_out_handle):
        Bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
        return Bool

    FOREGROUND_RED = 0x0c # red.
    FOREGROUND_GREEN = 0x0a # green.
    FOREGROUND_BLUE = 0x09 # blue.
    #reset white
    def resetColor():
        set_cmd_text_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)

    FOREGROUND_DARKRED = 0x04 # dark red.
    FOREGROUND_DARKGREEN = 0x02 # dark green.
    FOREGROUND_DARKSKYBLUE = 0x03 # dark skyblue.

    class printColor:
        def __exit__(self,*args,**kwargs):
            resetColor()

    class printDarkRed(printColor):
        def __enter__(self):
            set_cmd_text_color(FOREGROUND_DARKRED)

    #暗绿色
    #dark green
    class printDarkGreen(printColor):
        def __enter__(self):
            set_cmd_text_color(FOREGROUND_DARKGREEN)

    #暗天蓝色
    #dark sky blue
    class printDarkSkyBlue(printColor):
        def __enter__(self):
            set_cmd_text_color(FOREGROUND_DARKSKYBLUE)



elif islinux():
    STYLE = {
        'fore':
        {
            'red'      : 31,   #  红色
            'green'    : 32,   #  绿色
            'cyan'     : 36,   #  青蓝色
        },

    }


    def UseStyle(string, fore=''):

        fore  = '%s' % STYLE['fore'][fore] if fore in STYLE['fore'] else ''

        style = ';'.join([s for s in [fore] if s])

        style = '\033[%sm' % style if style else ''

        return '%s%s' % (style, string)


################################################################################


if __name__=='__main__':

    interactive()

