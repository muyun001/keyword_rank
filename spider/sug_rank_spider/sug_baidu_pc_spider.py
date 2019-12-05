# -*- coding: utf-8 -*-
"""
 @Time: 2017/8/9 14:49
 @Author: sunxiang
"""
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
from base_rank_spider import BaseSugRankSpider
from util.device_enums import DeviceEnums
from spider.page_rank_spider.build_id.baidu_id_build import Baidu_id_build
from util.useragent import UserAgentUtil
from util.search_type_enums import SearchTypeEnums
from extractor.sug_rank.sug_baidu_pc_extractor import SugBaiduPCExtractor

class SugBaiduPCSpider(BaseSugRankSpider):
    """
        百度PC下拉
    """
    def __init__(self):
        super(SugBaiduPCSpider, self).__init__()
        self.search_device = DeviceEnums.sug_baidu_pc
        self.extractor = SugBaiduPCExtractor()

    def get_request_param(self, task_id, keyword, target_url, keyword_id):
         configs = {"store_type": 2, "priority": 3}
         url = "https://www.baidu.com/sugrec?pre=1&p=3&ie=utf-8&json=1&prod=pc&from=wise_web&wd={}&req=2&csor=6".format(keyword)
         urls = [{
             'url': url,
             'type': SearchTypeEnums.UrlNotEqual.value,
             'keyword': keyword,
             'ckurl': target_url,
             'id': task_id,
             "unique_key": self.get_unique_key(),
             "search_device": self.search_device.name,
             "keyword_id": keyword_id}]

         return {"configs": configs, "urls": urls}


def Main():
    spider = SugBaiduPCSpider()
    # Thread(target=spider.clear_urls).start()
    # Thread(target=spider.reset_task).start()

    spider.run(8, 5, 5, 2, -1, -1, -1, -1, False)
    # spider.run(1, 1, 1, 1, 600, 600, 600, 600, True)

if __name__ == '__main__':
    Main()
