# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""
download tie from Baidu Tieba
"""

import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import http.client
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
    def __init__(self, baseUrl, seeLZ=True, floorTag=True, output_dir='.',
                 proxy=None):

        #base链接地址
        self.baseURL = baseUrl
        #是否只看楼主
        seeLZ_param = 1 if seeLZ else 0
        self.seeLZ = seeLZ
        self.seeLZ_str = '?see_lz='+str(seeLZ)
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

        if proxy != None:
            from minghu6.internet.proxy_ip import proxy_ip
            test_url = 'http://tieba.baidu.com/'
            if proxy_ip.install_proxy_opener(dbname=proxy,
                                             test_url=test_url,
                                             allow_delete=False) == None:

                raise Exception("Can't find proxy ip for url {0}".format(test_url))

    #传入页码，获取该页帖子的代码
    def getPage(self, pageNum):

        #构建URL
        if pageNum == 0:
            url = self.baseURL
        else:
            url = self.baseURL+ self.seeLZ_str + '&pn=' + str(pageNum)

        try:
            request = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(request, timeout=600)

            content = None
            while True:
                try:
                    content = response.read()
                except http.client.IncompleteRead as ex:
                    color.print_warn(ex)
                    color.print_info('retry...')
                else:
                    break

            #返回UTF-8格式编码内容
            return content.decode('utf-8')

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

    @staticmethod
    def get_name_by_id(id):
        url='http://tieba.baidu.com/home/main?id={0:s}&fr=userbar'.format(id)
        try:
            request = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(request)
            #返回GBK格式编码内容
            content = response.read().decode('gbk')
            #print(id)
            pattern = re.compile("(?<=<title>).+(?=的贴吧</title>)")
            result = re.search(pattern, content).group(0)


        #无法连接，报错
        except urllib.error.URLError as e:
            if hasattr(e,"reason"):
                print("Failed to connect to BaiDuTieBa,Error Reason", e.reason)
                return None
        except AttributeError:
            name = 'not find'
            return name
        else:
            return result
    #获取每一层楼的内容,传入页面内容
    def getContent(self, page):
        #匹配所有楼层的内容
        pattern = re.compile('<div id="post_content_.*?>(.*?)</div>')
        items = re.finditer(pattern, page)
        contents = []
        for item in items:
            #将文本进行去除标签处理，同时在前后加入换行符
            content = "\n"+self.tool.replace(item.group(0))+"\n"
            if not self.seeLZ:
                id_pattern = r'(?<=post_content_)(\d)+(?=")'
                id = re.search(id_pattern, item.group(0)).group(0)
                name = BDTB.get_name_by_id(id)
                contents.append((content, id, name))
            else:
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
        if hasattr(self, 'file') and self.file != None:
            self.file.close()



    def writeData(self,contents):
        #向文件写入每一楼的信息
        for item in contents:

            if not self.seeLZ:
                id, name = item[1:3]
                reply_user = '\n{0} {1}:\n'.format(id, name)
                #print(reply_user)
                self.file.write(reply_user)
                item = item[0]
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


        # Write LZ ID and NAME
        pattern = re.compile('<div id="post_content_.*?>(.*?)</div>')
        items = re.finditer(pattern, content)
        item = next(items)
        id_pattern = r'(?<=post_content_)(\d)+(?=")'
        lz_id = re.search(id_pattern, item.group(0)).group(0)
        #print(lz_id)
        lz_name = BDTB.get_name_by_id(lz_id)

        splitLine = "="*80 + '\n'
        self.file.write(splitLine)
        self.file.write('LZ {0} {1}\n'.format(lz_id, lz_name))
        self.file.write(splitLine)



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


def main(tieids, notseeLZ=False, notfloorTag=False, output_dir='.',
         proxy=False, dbname=None):

    if proxy:
        from minghu6.internet.proxy_ip import RESERVERD_DB_NAME
        if dbname==None:
            proxy = RESERVERD_DB_NAME
        else:
            proxy = dbname

    else:
        proxy = None


    for tieid in tieids:
        baseURL = 'http://tieba.baidu.com/p/'+str(tieid)
        bdtb = BDTB(baseUrl=baseURL,
                    seeLZ=not notseeLZ,
                    floorTag=not notfloorTag,
                    output_dir=output_dir,
                    proxy=proxy)

        bdtb.start()
        print()




def interactive():
    from argparse import ArgumentParser

    parser = ArgumentParser()

    parser.add_argument('tieids', nargs='+',
                        help='supply your tie id')

    parser.add_argument('-notonlylz', '--notonlylz', dest='notseeLZ', action='store_true',
                        help='not only care about LouZhu')

    parser.add_argument('-notshow_floor', '--notshow_floor', dest='notfloorTag',
                        action='store_true',
                        help='not show floor number')

    parser.add_argument('-o', '--output_dir', default='.',
                        help='point a outpur dir')

    parser.add_argument('-proxy', '--proxy', action='store_true',
                        help='use proxy ip')

    parser.add_argument('-db', '--dbname', default=None,
                        help='point another proxy db (optional)')



    args = parser.parse_args().__dict__
    #print(args)
    main(**args)

if __name__ == '__main__':

    interactive()


























