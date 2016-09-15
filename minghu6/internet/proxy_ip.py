# -*- Coding:utf-8 -*-
#!/usr/bin/env python3

"""
get proxy ip in china high anonymous
(need lxml, en.. can intead by bs4, but i'm late to change)
"""

import urllib.request
import urllib.error
import time
import datetime
from lxml import etree
import sqlite3,time
import traceback

from minghu6.http.request import headers
from minghu6.algs.metaclass import singleton_basic
from minghu6.text.color import color

class singleton_dbname(singleton_basic):

    def _getkey(cls, *args, **kwargs):
        dbname = args[0] if len(args)>0 else kwargs['dbname']
        return dbname

import os
import re
pat = r"minghu6[\\/]"

resource_path = os.path.join(re.split(pat, __file__)[0], 'resources')



class proxy_ip(object, metaclass=singleton_dbname):

    def __init__(self, dbname = None):

        from minghu6.http.request import headers
        self.header = headers
        create_tb='''
        CREATE TABLE IF NOT EXISTS PROXY
        (DATE DATETIME NOT NULL,
        IP CHARACTER(15),
        PORT INTEGER,
        REGION TEXT NOT NULL,
        PRIMARY KEY(IP, PORT)
        );
        '''
        if dbname == None or dbname=='proxy.db':
            dbname = os.path.join(resource_path, 'proxy.db')

        try:
            conn=sqlite3.connect(dbname)
        except sqlite3.OperationalError as opex:
            color.print_err(opex)
            color.print_err('dbname : {0:s}'.format(dbname))

        self.conn = conn
        self.dbname = dbname
        conn.execute(create_tb)

    def __del__(self):
        self.conn.close()

    def __enter__(self, *args):
        return self

    def __exit__(self, *args):
        self.conn.close()

    def try_get_root(self, num, timeout=5):

        nn_url = "http://www.xicidaili.com/nn/" + str(num)
        #国内高匿
        req = urllib.request.Request(nn_url, headers=headers)
        ip_set = self.get_ip_port(region='china')

        for ip,port in ip_set:
            try:
                proxy={'http':'{0}:{1}'.format(ip, port)}
                color.print_info ('\ntry '+proxy['http']+'\n')

                #使用这个方式是全局方法。
                proxy_support=urllib.request.ProxyHandler(proxy)
                opener=urllib.request.build_opener(proxy_support)
                urllib.request.install_opener(opener)


                resp = urllib.request.urlopen(req, timeout=timeout)
            except Exception as ex:
                if not self.isAlive(ip, port):
                    self.delete_db(ip, port)
            else:
                color.print_ok('Connect server OK!')
                return resp

        try:

            #使用这个方式是全局方法。
            proxy_support=urllib.request.ProxyHandler(proxies=None)
            opener=urllib.request.build_opener(proxy_support)
            urllib.request.install_opener(opener)

            resp = urllib.request.urlopen(req, timeout=timeout)
        except urllib.error.URLError as ex:

            return None
        else:
            color.print_ok('Connect server OK!')
            return resp

    def getContent(self, num, timeout=10):

        resp = self.try_get_root(num=num)
        if resp == None:
            nn_url = "http://www.xicidaili.com/nn/" + str(num)
            raise Exception('Can not connect to {0}'.format(nn_url))

        content = resp.read()
        resp.close()

        et = etree.HTML(content)
        result_even = et.xpath('//tr[@class=""]')
        result_odd = et.xpath('//tr[@class="odd"]')
        #因为网页源码中class 分开了奇偶两个class，所以使用lxml最方便的方式就是分开获取。
        #刚开始我使用一个方式获取，因而出现很多不对称的情况，估计是网站会经常修改源码，怕被其他爬虫的抓到
        #使用上面的方法可以不管网页怎么改，都可以抓到ip 和port
        now = time.strftime("%Y-%m-%d")
        for i in result_even:
            t1 = i.xpath("./td/text()")[:3]
            region = '台湾' if t1[2].find('台湾')!=-1 else '中国大陆'

            color.print_info("IP:%s\tPort:%s\tRegion:%s"%(t1[0],t1[1],region))
            if self.isAlive(t1[0], t1[1], region, timeout=timeout):
                self.insert_db(now,t1[0],t1[1],region)
            else:
                self.delete_db(ip=t1[0], port=t1[1])

        for i in result_odd:
            t2 = i.xpath("./td/text()")[:3]

            region = '台湾' if t2[2].find('台湾')!=-1 else '中国大陆'
            color.print_info ("IP:%s\tPort:%s\tRegion:%s" % (t2[0], t2[1], region))
            if self.isAlive(t2[0], t2[1], region, timeout=timeout):
                self.insert_db(now,t2[0],t2[1],region)
            else:
                self.delete_db(ip=t2[0], port=t2[1])

    def insert_db(self, date, ip, port, region):

        conn = self.conn
        insert_db_cmd='''
        INSERT INTO PROXY (DATE,IP,PORT,REGION) VALUES ('%s','%s','%s','%s');
        ''' %(date,ip,port,region)
        try:
            conn.execute(insert_db_cmd)
        except sqlite3.IntegrityError:
            pass
        else:
            conn.commit()

    def delete_db(self, ip, port):
        conn = self.conn
        delete_db_cmd = 'DELETE FROM PROXY WHERE IP=? AND PORT=?'
        conn.execute(delete_db_cmd, (ip, port))

    def commit_db(self):
        self.conn.commit()

    def get_ip_port(self, region='china', date=None):
        exec_sql = 'SELECT IP, PORT FROM PROXY WHERE REGION like ?'

        conn = self.conn
        cur = conn.cursor()
        cur.execute(exec_sql, (region,))

        return cur.fetchall()

    def loop(self, page=5, timeout=10):
        for i in range(1, page+1):
            try:
                self.getContent(i, timeout=timeout)
            except Exception as ex:
                color.print_err(ex)

    #查看爬到的代理IP是否还能用
    def isAlive(self, ip, port, region='中国大陆', timeout=3):
        proxy={'http':'{0}:{1}'.format(ip, port)}
        #print (proxy['http'], region)
        inside = {'中国大陆',
                  'china', }

        outside = {'台湾',
                  'taiwan',}



        #使用这个方式是全局方法。
        proxy_support=urllib.request.ProxyHandler(proxy)
        opener=urllib.request.build_opener(proxy_support)
        urllib.request.install_opener(opener)

        # google.com not work ...
        test_url="http://www.qq.com" if region in inside else 'https://www.baidu.com/'
        req=urllib.request.Request(test_url,headers=headers)
        try:

            resp=urllib.request.urlopen(req,timeout=timeout)

            if resp.code==200:
                color.print_ok("work")
                return True
            else:
                color.print_err("not work")
                return False

        except :
            color.print_err("Not work")
            return False

    #查看数据库里面的数据时候还有效，没有的话将其纪录删除
    def check_db_pool(self):
        self.conn.close()
        self.conn = sqlite3.connect(self.dbname)

        conn =self.conn
        query_cmd='''
        select IP,PORT,REGION from PROXY;
        '''
        cursor=conn.execute(query_cmd)
        for row in cursor:
            if not self.isAlive(row[0],row[1],row[2]):
                #代理失效， 要从数据库从删除
                delete_cmd='''
                delete from PROXY where IP='%s'
                ''' %row[0]
                color.print_warn ("delete IP %s in db" %row[0])
                conn.execute(delete_cmd)
                conn.commit()

        conn.close()




if __name__ == '__main__':
    #proxy = proxy_ip('proxy.db')
    #proxy.loop(page=3)
    #proxy.check_db_pool()

    #print('__file__ {0}'.format(__file__))
    print(resource_path)

    #p1 = proxy_ip(dbname='test2.sqlite3')
    #p2 = proxy_ip(dbname='test3.sqlite3')

    #print(p1 is p2)