# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""
download tie from Baidu Tieba
"""

import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import re
import os

from minghu6.http.request import headers
from minghu6.text.color import color

#处理页面标签类
class Tool:
    #去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    #删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    #把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    #将表格制表<td>替换为\t
    replaceTD= re.compile('<td>')
    #把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    #将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    #将其余标签剔除
    removeExtraTag = re.compile('<.*?>')

    @staticmethod
    def replace(x):
        x = re.sub(Tool.removeImg,"",x)
        x = re.sub(Tool.removeAddr,"",x)
        x = re.sub(Tool.replaceLine,"\n",x)
        x = re.sub(Tool.replaceTD,"\t",x)
        x = re.sub(Tool.replacePara,"\n    ",x)
        x = re.sub(Tool.replaceBR,"\n",x)
        x = re.sub(Tool.removeExtraTag,"",x)
        #strip()将前后多余内容删除
        return x.strip()



#百度贴吧爬虫类
class BDTB:

    #初始化，传入基地址，是否只看楼主的参数
    def __init__(self, baseUrl, seeLZ=True, floorTag=True, output_dir='.'):
        #base链接地址
        self.baseURL = baseUrl
        #是否只看楼主
        seeLZ_param = 1 if seeLZ else 0
        self.seeLZ = '?see_lz='+str(seeLZ)
        #HTML标签剔除工具类对象
        self.tool = Tool
        #全局file变量，文件写入操作对象
        self.file = None
        #楼层标号，初始为1
        self.floor = 1
        #默认的标题，如果没有成功获取到标题的话则会用这个标题
        path = urllib.request.urlsplit(self.baseURL).path
        self.tie_id = os.path.split(path)[-1]
        self.defaultTitle = self.tie_id
        #是否写入楼分隔符的标记
        self.floorTag = floorTag
        #设置输出目录路径
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        self.output_dir = output_dir

    #传入页码，获取该页帖子的代码
    def getPage(self, pageNum):

        #构建URL
        if pageNum == 0:
            url = self.baseURL
        else:
            url = self.baseURL+ self.seeLZ + '&pn=' + str(pageNum)

        try:
            request = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(request, timeout=7)
            #返回UTF-8格式编码内容
            return response.read().decode('utf-8')
        #无法连接，报错
        except urllib.error.URLError as e:
            if hasattr(e, "reason"):
                color.print_err("Failed to connect to BaiDuTieBa, Error Reason",e.reason)
                return None

    #获取帖子标题
    def getTitle(self, page):
        #得到标题的正则表达式
        pattern = re.compile(r'<h(\d)(\W)+class="core_title_txt.*>(.*)</h\1>')
        result = re.search(pattern,page)
        if result:
            #如果存在，则返回标题
            result = result.group(0)
            pattern2=r'(?<=>)(.*)(?=</h\d>)'
            result2 = re.search(pattern2, result).group(0).strip()
            #bs4.BeautifulSoup(matched_result, 'html.parser').text.strip()
            return result2

        else:
            return None

    #获取帖子一共有多少页
    def getPageNum(self, page):
        #获取帖子页数的正则表达式
        pat1=re.compile(r'<li(\W)+class="l_reply_num.*</span>.*<span.*>(.*)</span>')
        result=re.search(pat1, page).group(0)

        pat2=re.compile(r"回复贴，(\W)*共<span(\W)+.*>(\d)+</span>")
        result2=re.search(pat2, result).group(0)

        pat3=r"(?<=>)(\d)+(?=</span>)"
        result3=re.search(pat3, result2).group(0)

        return int(result3)

    #获取每一层楼的内容,传入页面内容
    def getContent(self, page):
        #匹配所有楼层的内容
        pattern = re.compile('<div id="post_content_.*?>(.*?)</div>')
        items = re.finditer(pattern,page)
        contents = []
        for item in items:
            #将文本进行去除标签处理，同时在前后加入换行符
            content = "\n"+self.tool.replace(item.group(0))+"\n"
            contents.append(content)
        return contents

    def openFile(self, title):
        #如果标题不是为None，即成功获取到标题
        if title is not None:
            path = os.path.join(self.output_dir, title) + ".txt"
            self.file = open(path, "w", encoding='utf-8')
        else:
            path = os.path.join(self.output_dir, self.defaultTitle) + ".txt"
            self.file = open(self.defaultTitle + ".txt","w", encoding='utf-8')


    def closeFile(self):
        self.file.close()

    def __del__(self):
        if hasattr(self, 'file'):
            self.file.close()



    def writeData(self,contents):
        #向文件写入每一楼的信息
        for item in contents:
            if self.floorTag:
                #楼之间的分隔符
                floorLine = "\n" + str(self.floor) + '='*80 + '\n'

                self.file.write(floorLine)
            self.file.write(item)
            self.floor += 1

    def start(self):
        color.print_info('start analyse..., url {0:s}'.format(self.baseURL))
        content = self.getPage(0)
        pageNum = self.getPageNum(content)
        title = self.getTitle(content)
        self.openFile(title)
        if pageNum == None:
            color.print_err("the URL {0:s} might be invalidated".format(self.baseURL))
            return
        try:
            color.print_info("This tie {0:s} has {1:d} pages".format(title, pageNum))
            for i in range(1,int(pageNum)+1):
                color.print_info("write to page {0:d}".format(i))
                page = self.getPage(i)
                content = self.getContent(page)
                self.writeData(content)
        #出现写入异常
        except IOError as e:
            color.print_err(e)
        else:
            color.print_ok("Successful!")
        finally:
            self.closeFile()


def main(tieids, seeLZ=True, floorTag=True, output_dir='.'):

    for tieid in tieids:
        baseURL = 'http://tieba.baidu.com/p/'+str(tieid)
        bdtb = BDTB(baseUrl=baseURL,
                    seeLZ=seeLZ,
                    floorTag=floorTag,
                    output_dir=output_dir)
        bdtb.start()
        print()




def interactive():
    from argparse import ArgumentParser

    parser = ArgumentParser()

    parser.add_argument('tieids', nargs='+',
                        help='supply your tie id')

    parser.add_argument('-onlylz', '--onlylz', dest='seeLZ',
                        type=bool, default=True,
                        help='only care about LouZhu (default=True)')

    parser.add_argument('-show_floor', '--show_floor', dest='floorTag',
                        type=bool, default=True,
                        help='show floor no (default=True)')

    parser.add_argument('-o', '--output_dir', default='.',
                        help='point a outpur dir')

    args = parser.parse_args().__dict__

    main(**args)

if __name__ == '__main__':

    interactive()


























