# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""
Youtube download Tools
"""
import os
import urllib.error


from minghu6.io.stdio import askyesno

from minghu6.text.color.color_cmd import printDarkSkyBlue,printDarkRed,printDarkGreen
from minghu6.text.SequenceEnhance import filter_invalid_char
def __get_video(v_id):
    import requests
    url='https://www.youtube.com/watch?v='+str(v_id)
    res=requests.get(url)

    import re
    pat_json=re.compile('"args":({.*?})')
    m_json=re.search(pat_json,res.text)

    pat_title=re.compile('(?<=<title>).*(?=</title>)')
    m_title=re.search(pat_title,res.text)

    title=m_title.group(0)
    res.close()

    import json
    jd=json.loads(m_json.group(1))
    #print(jd['url_encoded_fmt_stream_map'])

    from urllib.parse import parse_qs
    a=parse_qs(jd['url_encoded_fmt_stream_map'])


    return title,a['quality'],a['url']


err_dict=dict()
resolution_map={'720p':'hd720',
                'medium':'medium'}

RESOLUTION_TOO_LOW='Resolution is too Low'
V_NOT_EXIST='Video Not Exist'
URL_TIME_OUT='Url Time Out'
def get_video(v_id,output_dir='',resolution='720p',tourl=None):

    try:
        title,quality_l,url_l=__get_video(v_id)
    except Exception as ex:
        err_dict[v_id]=ex
        printDarkRed(ex)
        return



    def match_resolution(quality_l,resolution):

        minimum=resolution_map[resolution]

        for quality in quality_l:
            if minimum in quality:
                return True

        return False
    if not match_resolution(quality_l,resolution):
        printDarkRed(RESOLUTION_TOO_LOW)
        err_dict[v_id]=RESOLUTION_TOO_LOW
        return

    url=url_l[0]
    if tourl!=None:
        with open(tourl,'a') as f:
            #with import print_function,so python2 can run it too.
            print('#'+v_id,file=f)
            print('#'+title,file=f)
            print(url,file=f)
            print(file=f)
            print(file=f)

        return

    import traceback
    from urllib.request import urlretrieve
    from minghu6.http.urlretrieve import report_color

    def format_filename(title):
        return filter_invalid_char(title)+'.mp4'

    filename=format_filename(title)
    try:

        #some shell codec like Cinese Simplied Windows's gbk
        #    can not decode some unicode character
        ps=':) downloading %s \t'
        ps=ps%title
        printDarkSkyBlue(ps)

        try:
            fullfn=os.path.join(output_dir,filename)
            #print(fullfn)
            if os.path.exists(fullfn) and \
                    not askyesno('find Same name file,Overload?'):
                    err_dict[v_id]=fullfn

            else:
                ################################################################
                #DownLoad !!#

                try:
                    urlretrieve(url=url,
                                filename=fullfn,
                                reporthook=report_color)
                except urllib.error.HTTPError as ex:
                    printDarkRed(ex)
                    printDarkRed('\nNow dressed as a Web Browser...')

                    def urlretrieve2():
                        import requests
                        import shutil

                        from minghu6.http.request import headers
                        res=requests.get(url,stream=True,headers=headers)
                        with open(fullfn,'wb') as f:
                            shutil.copyfileobj(res.raw, f)
                    urlretrieve2()

                from minghu6.etc.path import isempty_file
                if isempty_file(fullfn):
                    os.remove(fullfn)
                    #os.remove(os.path.splitext(fullfn)[0])
                    err_dict[v_id]=URL_TIME_OUT
                    return
                ################################################################
        except Exception as ex:
            err_dict[v_id]=V_NOT_EXIST
            traceback.print_exc()

    except Exception as ex:

        traceback.print_exc()
        pts='\n:( Sorry! The action is failed.\n'
        printDarkRed(pts)

        err_dict[v_id]=title


def get_videos(v_ids,filename=None,output_dir='',resolution='720p',tourl=None):

    v_ids=set(v_ids)
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
            printDarkRed(ex)


    for (i,v_id) in enumerate(v_ids):
        if tourl==None:
            pts='\nDownloading ({0:d}/{1:d}) file'.format(i+1,len(v_ids))
        else:
            pts='\nGeting ({0:d}/{1:d}) urls '.format(i+1,len(v_ids))

        printDarkSkyBlue(pts)
        try:
            get_video(v_id,output_dir,resolution,tourl)
        except Exception as ex:
            printDarkRed(ex)

        print()

    if len(err_dict)==0:

        if tourl==None:
            pts='\n\nDownload complete.'
        else:
            pts='\nGet url complete'

        printDarkGreen(pts)

    else:
        total_num=len(v_ids)
        failed_num=len(err_dict)
        print('\n\n')

        pts1='total: \t\t%d'%total_num
        pts2='succeed:\t%d'%(total_num-failed_num)
        pts3='failed:\t\t%d'%failed_num

        printDarkSkyBlue(pts1)
        printDarkGreen(pts2)
        printDarkRed(pts3)

        print()

        for key in err_dict:
            pts='{0} : {1} failed\t'.format(key,err_dict[key])
            printDarkRed(pts)



def interactive():
    from argparse import ArgumentParser

    parser=ArgumentParser()

    parser.add_argument('-f','--file',dest='filename',
                        help=('pass masses of video id in form of csv file\n'
                              '(can not use with v_ids at the same time)\n'
                              'ascii comm!! for python2'))

    parser.add_argument('v_ids',nargs='*',
                        help='pass video ids(can not use with -f at the same time)')

    parser.add_argument('-o','--output_dir',
                        help='output video directory')

    parser.add_argument('-r','--resolution',default='720p',choices=['720p','medium'],
                        help='the minimum resolution you can accept (default 720p)')

    parser.add_argument('-t','--tourl',
                        help='point a file to save the url')


    args=parser.parse_args().__dict__
    #print(args)

    if args['output_dir']!=None:
        args['output_dir']=os.path.abspath(args['output_dir'])
        if not os.path.isdir(os.path.abspath(args['output_dir'])):
            raise Exception('arg: -o/--output_dir is not a valid directory')
    else:
        args['output_dir']=''
    if args['filename']==None and args['v_ids'].__len__()==0:
        raise Exception('too few args need -f or v_ids')


    get_videos(**args)

if __name__ == '__main__':
    interactive()