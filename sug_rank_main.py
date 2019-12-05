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
from  spider.sug_rank_spider.sug_baidu_pc_spider import SugBaiduPCSpider
from  spider.sug_rank_spider.sug_baidu_mobile_spider import SugBaiduMobileSpider
from  spider.sug_rank_spider.sug_360_pc_spider import Sug360PCSpider
from  spider.sug_rank_spider.sug_360_mobile_spider import Sug360MobileSpider
from  spider.sug_rank_spider.sug_sogou_pc_spider import SugSogouPCSpider
from  spider.sug_rank_spider.sug_sogou_mobile_spider import SugSogouMobileSpider
from  spider.sug_rank_spider.sug_sm_mobile_spider import SugSmMobileSpider


def Main():
    # Thread(target=spider.clear_urls).start()

    baidu_pc_spider = SugBaiduPCSpider()
    baidu_pc_spider.run(2, 1, 1, 1, -1, -1, -1, -1, False)

    baidu_mobile_spider = SugBaiduMobileSpider()
    baidu_mobile_spider.run(2, 1, 1, 1, -1, -1, -1, -1, False)

    so_pc_spider = Sug360PCSpider()
    so_pc_spider.run(2, 1, 1, 1, -1, -1, -1, -1, False)

    so_mobile_spider = Sug360MobileSpider()
    so_mobile_spider.run(2, 1, 1, 1, -1, -1, -1, -1, False)

    sogou_pc_spider = SugSogouPCSpider()
    sogou_pc_spider.run(2, 1, 1, 1, -1, -1, -1, -1, False)

    sogou_mobile_spider = SugSogouMobileSpider()
    sogou_mobile_spider.run(2, 1, 1, 1, -1, -1, -1, -1, False)

    sm_mobile_spider = SugSmMobileSpider()
    sm_mobile_spider.run(2, 1, 1, 1, -1, -1, -1, -1, False)

if __name__ == '__main__':
    Main()