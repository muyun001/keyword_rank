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
from  spider.page_rank_spider.baidu_pc_spider import BaiduPCSpider
from  spider.page_rank_spider.baidu_mobile_spider import BaiduMobileSpider
from  spider.page_rank_spider.so_pc_spider import SoPCSpider
from  spider.page_rank_spider.sogou_pc_spider import SogouPCSpider
from  spider.page_rank_spider.sm_mobile_spider import SmMobileSpider

def Main():
    # Thread(target=spider.clear_urls).start()

    baidu_pc_spider = BaiduPCSpider()
    baidu_pc_spider.run(4, 4, 20, 20, -1, -1, -1, -1, False)

    baidu_mobile_spider = BaiduMobileSpider()
    baidu_mobile_spider.run(4, 4, 20, 20, -1, -1, -1, -1, False)

    so_pc_spider = SoPCSpider()
    so_pc_spider.run(4, 4, 20, 20, -1, -1, -1, -1, False)

    sogou_pc_spider = SogouPCSpider()
    sogou_pc_spider.run(4, 4, 20, 20, -1, -1, -1, -1, False)

    sm_mobile_spider = SmMobileSpider()
    sm_mobile_spider.run(4, 4, 20, 20, -1, -1, -1, -1, False)

if __name__ == '__main__':
    Main()
