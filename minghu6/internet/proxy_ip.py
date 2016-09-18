# -*- coding:utf-8 -*-
#!/usr/bin/env python3

"""
get proxy ip in china high anonymous
(need lxml（recommend） or beautifulsoup4 )
"""

import sqlite3
import time
import urllib.error
import urllib.request
import traceback

from minghu6.algs.metaclass import singleton_basic
from minghu6.http.request import headers
from minghu6.text.color import color


RESERVERD_DB_NAME = 'proxy.db'

class singleton_dbname(singleton_basic):

    def _getkey(cls, *args, **kwargs):
        dbname = args[0] if len(args)>0 else kwargs['dbname']

        if dbname == RESERVERD_DB_NAME:
            dbname = None

        return dbname

import os
import re
pat = r"minghu6[\\/]"

resource_path = os.path.join(re.split(pat, __file__)[0], 'resources')



class proxy_ip(object, metaclass=singleton_dbname):

    def __init__(self, dbname = None, debug=False):

        self.debug = debug
        from minghu6.http.request import headers
        self.header = headers
        create_tb= ('\n'
                    '        CREATE TABLE IF NOT EXISTS PROXY\n'
                    '        (DATE DATETIME NOT NULL,\n'
                    '        IP CHARACTER(15),\n'
                    '        PORT INTEGER,\n'
                    '        REGION TEXT NOT NULL,\n'
                    '        PRIMARY KEY(IP, PORT)\n'
                    '        );\n'
                    '        ')
        if dbname == None or dbname== RESERVERD_DB_NAME:
            dbname = os.path.join(resource_path, RESERVERD_DB_NAME)

        try:
            conn=sqlite3.connect(dbname)
        except sqlite3.OperationalError as opex:
            color.print_err(opex)
            color.print_err('dbname : {0:s}'.format(dbname))
            raise Exception()

        else:
            self.conn = conn
            self.dbname = dbname
            conn.execute(create_tb)
            color.print_ok('conect to the db {0}'.format(dbname))
            try:
                import lxml
            except ImportError:
                self.parse_ip_port_region = proxy_ip.parse_ip_port_region_httpparser
            else:
                self.parse_ip_port_region = proxy_ip.parse_ip_port_region_lxml

    def __del__(self):
        self.conn.close()

    def __enter__(self, *args):
        return self

    def __exit__(self, *args):
        self.conn.close()


    @staticmethod
    def parse_ip_port_region_lxml(content):
        from lxml import etree
        data_set = set()

        et = etree.HTML(content)
        result_even = et.xpath('//tr[@class=""]')
        result_odd = et.xpath('//tr[@class="odd"]')
        #因为网页源码中class 分开了奇偶两个class，所以使用lxml最方便的方式就是分开获取。
        #刚开始我使用一个方式获取，因而出现很多不对称的情况，估计是网站会经常修改源码，怕被其他爬虫的抓到
        #使用上面的方法可以不管网页怎么改，都可以抓到ip 和port
        for i in result_even:
            t1 = i.xpath("./td/text()")[:3]
            region = '台湾' if t1[2].find('台湾')!=-1 else '中国大陆'
            ip, port = t1[0:2]
            data_set.add((ip, port, region))


        for i in result_odd:
            t2 = i.xpath("./td/text()")[:3]
            region = '台湾' if t2[2].find('台湾')!=-1 else '中国大陆'
            ip, port = t2[0:2]
            data_set.add((ip, port, region))


        return data_set

    @staticmethod
    def parse_ip_port_region_httpparser(content):
        import bs4

        data_set = set()
        soup = bs4.BeautifulSoup(content, 'html.parser')
        results = soup.findAll(text=re.compile(r"^((\d+\.){3}(\d+)|\d+|(\W*台湾\W*))$"))
        ip_pattern = re.compile(r"^(\d+\.){3}(\d+)$")
        port_pattern =re.compile(r"^(\d){2}\d*$")
        region_pattern = re.compile(r'^\W*台湾\W*$')
        i=0

        while i < len(results):
            if re.match(ip_pattern, results[i]):
                ip = results[i]

            else:
                break

            port = results[i+1]
            if re.match(region_pattern, results[i+2]):
                region='taiwan'
                i += 3
            else:
                region='china'
                i += 2
            data_set.add((ip, port, region))
            #print(ip, port, region)

        return data_set

    @staticmethod
    def install_proxy_opener(region=('china', 'taiwan'), dbname=None, timeout=3):
        proxy_instance = proxy_ip(dbname=dbname)

        ip_set = proxy_instance.get_ip_port(region=region)

        for ip, port in ip_set:

            proxy = {'http': '{0}:{1}'.format(ip, port)}
            color.print_info('\ntry ')

            if not proxy_instance.isAlive(ip, port):
                proxy_instance.delete_db(ip, port)
                color.print_warn('not work, delete in db')

            else:
                # 使用这个方式是全局方法。
                proxy_support = urllib.request.ProxyHandler(proxy)
                opener = urllib.request.build_opener(proxy_support)
                urllib.request.install_opener(opener)

                # Then, you can use method urllib.request.urlopen()
                return ip, port

        return None


    def try_get_root(self, num, timeout=5):

        nn_url = "http://www.xicidaili.com/nn/" + str(num)
        #国内高匿
        req = urllib.request.Request(nn_url, headers=headers)

        result = proxy_ip.install_proxy_opener()
        if result != None:
            resp = urllib.request.urlopen(req, timeout=timeout)
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

        except Exception as ex:
                color.print_err(ex)
                if self.debug:
                    traceback.print_stack()
                    
        else:
            color.print_ok('Connect server OK!')
            return resp



    def getContent(self, num, timeout=3):

        resp = self.try_get_root(num=num)
        if resp == None:
            nn_url = "http://www.xicidaili.com/nn/" + str(num)
            raise Exception('Can not connect to {0}'.format(nn_url))

        content = resp.read()
        resp.close()

        data_set = self.parse_ip_port_region(content)
        now = time.strftime("%Y-%m-%d")
        for ip, port, region in data_set:

            #color.print_info("IP: %s\tPort: %s\tRegion: %s"%(ip, port, region))
            if self.isAlive(ip, port, region, timeout=timeout):
                self.insert_db(now, ip, port, region)
            else:
                self.delete_db(ip=ip, port=port)


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

    def get_ip_port(self, region=('china', 'taiwan'), date=None):

        exec_sql = 'SELECT IP, PORT FROM PROXY WHERE REGION like ?'
        conn = self.conn
        cur = conn.cursor()

        result = []
        if isinstance(region, (list, set, tuple)):

            for one_region in region:
                cur.execute(exec_sql, (one_region,))
                result += cur.fetchall()

        else:
            cur.execute(exec_sql, (region,))
            result = cur.fetchall()

        return result

    def loop(self, page=5, timeout=3):
        for i in range(1, page+1):
            try:
                self.getContent(i, timeout=timeout)
            except Exception as ex:
                color.print_err(ex)
                if self.debug:
                    traceback.print_stack()

    #查看爬到的代理IP是否还能用
    def isAlive(self, ip, port, region='中国大陆', timeout=3):
        proxy={'http':'{0}:{1}'.format(ip, port)}
        print(proxy['http'], region)
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