# -*- coding: utf-8 -*-
"""
 @Time: 2017/8/9 14:49
 @Author: sunxiang
"""
import datetime
import os
import sys

# PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
# sys.path.append(PROJECT_PATH)

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_PATH)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
reload(sys)
sys.setdefaultencoding('utf8')

import urllib
from spider.page_rank_spider.base_rank_spider import BaseRankSpider
from util.device_enums import DeviceEnums
from util.useragent import UserAgentUtil
from util.search_type_enums import SearchTypeEnums
from extractor.page_rank.so_pc_extractor import SoPCExtractor
from download_center.new_spider.util.util_md5 import UtilMD5

class SoPCSpider(BaseRankSpider):
    """
       360PC排名
    """
    def __init__(self):
        super(SoPCSpider, self).__init__()
        self.search_device = DeviceEnums.pc_360
        self.extractor = SoPCExtractor()

    def get_request_url(self, keyword, pn):
        kwh = {'q': keyword, "rc": "srp", "fr": "none"}
        if pn:
            kwh['pn'] = pn
        url = 'https://www.so.com/s?' + urllib.urlencode(kwh)
        return url

    def get_request_param(self, task_id, keyword, target_url, page, spidertype, keyword_id, site_name, pnum=1):
         nowtime = datetime.datetime.now()
         daystr = nowtime.strftime('%Y-%m-%d')
         key_source = '%s%s%s%s%s%s%s%s%s' % (daystr, task_id, keyword, target_url, page, spidertype, keyword_id, site_name, pnum)
         unique_key = UtilMD5.md5(key_source)
         configs = {"store_type": 2, "param": {"filter": 1}}
         if pnum != 1:
             configs['priority'] = 3

         headers = {'User-Agent': UserAgentUtil().random_one(self.search_device)}
         urls = [{
             'url': self.get_request_url(keyword, pnum),
             'type': 4 if spidertype == SearchTypeEnums.URLDomainCapture.value else 1,
             'keyword': keyword,
             'ckurl': target_url,
             'site_name': site_name,
             'id': task_id,
             "page": page,
             "unique_key": unique_key,
             "pnum": pnum,
             "search_device": self.search_device.name,
             "spidertype": spidertype,
             "keyword_id": keyword_id}]

         print(urls)

         return {"configs": configs, "headers": headers, "urls": urls}


def Main():
    spider = SoPCSpider()
    # Thread(target=spider.clear_urls).start()
    # Thread(target=spider.reset_task).start()

    spider.run(8, 5, 5, 2, -1, -1, -1, -1, False)
    # spider.run(1, 1, 1, 1, 600, 600, 600, 600, True)

if __name__ == '__main__':
    Main()
