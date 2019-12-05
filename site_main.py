# -*- coding: utf-8 -*-
"""
 @Time: 2017/8/9 14:49
 @Author: sunxiang
"""
import os
import sys
from threading import Thread

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_PATH)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
reload(sys)
sys.setdefaultencoding('utf8')
from download_center.store.store_mysql import StoreMysql
import config
import requests
import schedule
import time
from lxml.html import fromstring
from util.useragent import UserAgentUtil
from util.device_enums import DeviceEnums
from util.util_domain import DomainUtil

class SiteTask(object):

    def exec_sql(self, sql):
        db = StoreMysql(**config.baidu_spider_move)
        try:
            result = db.query(sql)
            db.close()
            return result
        except Exception:
            db.close()

    def update_sitename(self):
        print("start to update sitename ...")
        try:
            results = self.get_sites_by_no_name()
            if results:
                for item in results:
                    url = item[0]
                    name = self.get_baidupc_name(url)
                    domain = DomainUtil.get_domian(url)
                    if not name:
                        name = self.get_baidumobile_name(domain)

                    if name:
                        sql = "update task set site_name='{}' where url='{}'".format(name, url)
                        self.exec_sql(sql)
        except:
            print("update sitename error ...")
        print("update sitename finished ...")

    def get_sites_by_no_name(self):
        sql = "select distinct url from task where site_name is null"
        return self.exec_sql(sql)

    def get_baidupc_name(self, url):
        url = "http://www.baidu.com/s?ie=utf-8&wd=site%3A{}".format(url)
        headers = {
            'Connection': 'keep - alive',
            'User-Agent': UserAgentUtil().random_one(DeviceEnums.baidu_pc)
        }
        resp = requests.get(url, headers)
        tree = fromstring(resp.text)
        for i in range(1, 4):
            row_ele = tree.xpath('//*[@id="{}"]'.format(i))
            if len(row_ele):
                showurl_ele = row_ele[0].cssselect("a.c-showurl")
                if len(showurl_ele):
                    img_ele = showurl_ele[0].cssselect("img.source-icon")
                    if len(img_ele):
                        return img_ele[0].tail

    def get_baidumobile_name(self, url):
        url = "https://m.baidu.com/s?word=site:{}".format(url)
        headers = {
            'Connection': 'keep - alive',
            'User-Agent': UserAgentUtil().random_one(DeviceEnums.baidu_mobile)
        }
        resp = requests.get(url, headers)
        tree = fromstring(resp.text)
        results = tree.cssselect("div.result")
        for i in range(0, 3):
            if len(results) > i:
                row_ele = results[i]
                ele = row_ele.cssselect("span.c-color-gray")
                if len(ele) and not "总收录量" in ele[0].text:
                    return ele[0].text


    def run(self):
        schedule.every(1).days.do(self.update_sitename)
        while True:
            schedule.run_pending()
            time.sleep(60*60)

if __name__ == '__main__':
    st = SiteTask()
    st.run()