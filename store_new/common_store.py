# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 11:23:19 2016

@author: zhangle
"""
import os
import sys

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(PROJECT_PATH)
sys.path.append(os.path.join(PROJECT_PATH, 'new_spider'))
sys.path.append(os.path.join(PROJECT_PATH, 'store'))
sys.path.append(os.path.join(PROJECT_PATH, 'util'))

reload(sys)
sys.setdefaultencoding('utf8')

import redis
import json
import config


class CommonStore(object):

    def __init__(self):
        self.rds = redis.StrictRedis(**config.YUQING_REDIS)

    def store(self, results, name):
        key = results['key']
        del results['key']
        self.rds.hset(name, key, json.dumps(results))


if __name__ == '__main__':
    import time

    store = CommonStore()
    i = 1800
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    while True and i > 0:
        print int(store.rds.llen('html:task:common'))
        time.sleep(1)
        i -= 1
