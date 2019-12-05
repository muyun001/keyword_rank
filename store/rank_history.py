# -*- coding: utf-8 -*-
"""
 @Time: 2017/8/31 18:49
 @Author: sunxiang
"""
import config
from download_center.store.store_mysql import StoreMysql

import MySQLdb
import traceback
from datetime import datetime, timedelta


class RankHistoryStore(object):

    def save(self, device, keyword_id, rank):
        try:
            db = StoreMysql(**config.baidu_spider_move)
            sql = """insert into rank_daily(platform, out_id, rank, date, created_at, updated_at) values('{}', {}, {}, date(now()), now(), now())
    on duplicate key update updated_at = now(), rank = case when values(rank) between 1 and 10 then values(rank) else rank end""".format(device, keyword_id, rank)
            db.do(sql)
            db.close()
        except:
            print traceback.format_exc()
            db.close()


def test():
    pass
    # import config
    # sx = SourceStore(config.baidu_spider_move)
    # sx.delete_byid(607808, "task")


if __name__ == '__main__':
    test()
