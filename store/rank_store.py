# -*- coding: utf-8 -*-
"""
 @Time: 2017/8/31 18:49
 @Author: sunxiang
"""
import config
from download_center.store.store_mysql import StoreMysql

import MySQLdb
import traceback
import time
import re
from datetime import datetime, timedelta


class RankStore(object):
    def __init__(self):
        self.table = "task"
        self.reset_status()

    def reset_status(self):
        """
        查排名重启时重置还没拿到返回的task
        程序启动时，查找状态为1,并且更新时间为当天的条目，重置为状态0
        :return:
        """
        db = StoreMysql(**config.baidu_spider_move)
        reset_sql = 'update %s set status = 0 where status = 1 and datediff(now(), update_time) = 0' % self.table
        try:
            db.do(reset_sql)
        except Exception, e:
            print "reset_status error"
            print e
        finally:
            db.close()

    def find_task_lists(self, device, task_count):
        """
        获取查排名任务
        优先查询今日未查，但是已有排名rank<=reach_rank的任务
        :return:
        """
        task_results = self.get_yesterday_task_list(device, task_count)
        if task_results != -1:
            if len(task_results) < task_count:
                t_task_results = self.get_task_list(device, task_count)
                task_results = task_results + t_task_results
                if len(task_results) < task_count:
                    unreached_tasks = self.get_unreached_list(device, task_count)
                    task_results = task_results + unreached_tasks
        else:
            task_results = self.get_task_list(device, task_count)
            if len(task_results) < task_count:
                unreached_tasks = self.get_unreached_list(device, task_count)
                task_results = task_results + unreached_tasks

        # 更新状态 state
        if len(task_results) > 0:
            change_state_ids = list()
            for task in task_results:
                change_state_ids.append(task[0])
                if len(change_state_ids) == 50:
                    self.update_ids(self.table, change_state_ids)
                    change_state_ids = list()
            if len(change_state_ids) > 0:
                self.update_ids(self.table, change_state_ids)
        return task_results

    def get_yesterday_task_list(self, device, task_count):
        """
        获取昨日有排名的任务
        """
        reach_rank = config.reach_rank
        time_now = str(datetime.now()).split(" ")[0] + ' ' + config.time_now.strip()
        time_now_end = str(datetime.now()).split(" ")[0] + ' ' + config.time_now_end.strip()
        db = StoreMysql(**config.baidu_spider_move)
        try:
            query_sql = """select id, keyword, url, page, search_type, keyword_id, site_name
                        from task 
                        where device='{device}' and (rank between 0 and {reach_rank}) and ( status = 0 or ( datediff(now(), update_time) >= search_cycle and status in(1, 2) and now() > '{time_now}' and now() < '{time_now_end}' ))
                        order by update_time asc
                        limit {task_count}""".format(device=device, reach_rank=reach_rank, time_now=time_now, time_now_end=time_now_end, task_count=task_count)
            result = db.query(query_sql)
            db.close()
            return result
        except:
            print("get_yesterday_task_list error")
            traceback.print_exc()
            db.close()
            return -1

    def get_task_list(self, device, task_count):
        time_now = str(datetime.now()).split(" ")[0] + ' ' + config.time_now.strip()
        time_now_end = str(datetime.now()).split(" ")[0] + ' ' + config.time_now_end.strip()
        db = StoreMysql(**config.baidu_spider_move)
        try:
            sql = """select id, keyword, url, page, search_type, keyword_id, site_name
            from task 
            where device='{}' and ( status = 0 or ( datediff(now(), update_time) >= search_cycle and status in(1, 2) and now() > '{}' and now() < '{}' ))
            order by update_time asc 
            limit {}""".format(device, time_now, time_now_end, task_count)
            # print(sql)
            result = db.query(sql)
            db.close()
            return result
        except Exception:
            print traceback.format_exc()
            db.close()
            return -1

    def get_unreached_list(self, device, task_count):
        time_now = str(datetime.now()).split(" ")[0] + ' ' + config.time_now.strip()
        time_now_end = str(datetime.now()).split(" ")[0] + ' ' + config.time_now_end.strip()
        db = StoreMysql(**config.baidu_spider_move)
        search_count = config.search_count
        try:
            sql = """select id, keyword, url, {}, search_type, keyword_id, site_name
                    from task 
                    where device='{}' and status = 2 and (rank is null or rank not between 1 and 10) and search_count < {} and now() > '{}' and now() < '{}'
                    order by search_count asc 
                    limit {}""".format(1, device, search_count, time_now, time_now_end, task_count)
            result = db.query(sql)
            db.close()
            return result
        except Exception:
            print traceback.format_exc()
            db.close()
            return -1

    def store_table(self, results, table="", type=1, field=None):
        db = StoreMysql(**config.baidu_spider_move)
        try:
            if len(results) > 0:
                for result in results:
                    if type == 1:
                        for key in result:
                            result[key] = MySQLdb.escape_string(str(result[key]))
                        return_state = db.save(table, result)
                    elif type == 2:
                        for key in result:
                            result[key] = MySQLdb.escape_string(str(result[key]))
                        return_state = db.update(table, result, field)
                db.close()
                return return_state
        except Exception:
            print(traceback.format_exc())
            db.close()
            return -1

    # isupdate == 1 更新  2： pass
    def store_insert_or_update(self, results, table="", field=None, isupdate=1):
        db = StoreMysql(**config.baidu_spider_move)
        try:
            if len(results) > 0:
                for result in results:
                    values = ''
                    field_value = None
                    for key in result:
                        result[key] = MySQLdb.escape_string(str(result[key]))
                        if key == field:
                            field_value = result[key]
                        values += "%s='%s'," % (str(key), str(result[key]))
                    if field:
                        field_result = self.find_by_field(table, field, field_value)
                        if field_result:
                            if isupdate == 1:
                                return_state = db.update(table, result, field)
                            else:
                                pass
                        else:
                            db.save(table, result)
                    else:
                        db.save(table, result)
                if db:
                    db.close()
        except Exception:
            print(traceback.format_exc())
            db.close()
            return -1

    def find_by_field(self, table_name, field, field_value):
        db = StoreMysql(**config.baidu_spider_move)
        try:
            sql = "select * from %s where %s = %s " % (table_name, field, field_value)
            result = db.query(sql)
            db.close()
            return result
        except Exception:
            print traceback.format_exc()
            db.close()

    def store_table_db(self, results, table="", type=1, field=None, db_connnection=""):
        db = StoreMysql(**db_connnection)
        return_state = 0
        if len(results) > 0:
            for result in results:
                try:
                    if type == 1:
                        for key in result:
                            result[key] = MySQLdb.escape_string(str(result[key]))
                        return_state = db.save(table, result)
                    elif type == 2:
                        for key in result:
                            result[key] = MySQLdb.escape_string(str(result[key]))
                        db.update(table, result, field)
                except Exception, e:
                    print(traceback.format_exc())
                    return -1
                finally:
                    if db is not None:
                        db.close()
            return return_state

    def store_update(self, result, ty, field):
        i = 0
        for key in result:
            if result[key] and key != field:
                result[key] = MySQLdb.escape_string(str(result[key]))
                i += 1
        if i > 0:
            self.db.update(ty, result, field)

    def store_insert(self, result, ty):
        for key in result:
            result[key] = MySQLdb.escape_string(str(result[key]))
        self.db.save(ty, result)

    def deleteByids(self, ids, table=""):
        db = StoreMysql(**config.baidu_spider_move)
        try:
            for single_id in ids:
                sql = "delete from %s  where  id = %d " % (table, single_id['id'])
                db.do(sql)
            db.close()
        except:
            print traceback.format_exc()
            db.close()

    def update_ids(self, table_name, ids):
        db = StoreMysql(**config.baidu_spider_move)
        try:
            for single_id in ids:
                sql = "update  %s  set  status = 1, update_time = now(), search_count = case when date(now()) <> rank_date then 0 else search_count end  where id = %d  " % (table_name, single_id)
                db.do(sql)
            db.close()
        except Exception:
            print traceback.format_exc()
            db.close()

    def delete_by_id(self, table_name, table_id):
        db = StoreMysql(**config.baidu_spider_move)
        try:
            sql = "delete from %s where id = %d" % (table_name, table_id)
            db.do(sql)
            db.close()
        except Exception:
            print traceback.format_exc()
            db.close()

    def find_rank_by_taskid(self, table_name, table_id):
        db = StoreMysql(**config.baidu_spider_move)
        try:
            sql = "select * from %s where taskId = %d " % (table_name, table_id)
            result = db.query(sql)
            db.close()
            return result
        except Exception:
            print traceback.format_exc()
            db.close()

    def find_task_by_id(self, table_name, table_id):
        db = StoreMysql(**config.baidu_spider_move)
        try:
            sql = "select * from %s where id = %d " % (table_name, table_id)
            result = db.query(sql)
            db.close()
            return result
        except Exception:
            print traceback.format_exc()
            db.close()

    def reset_task(self, interval_time):
        db = StoreMysql(**config.baidu_spider_move)
        try:
            expire_time = str(datetime.now() + timedelta(seconds=-interval_time))
            sql = "update {} set status = 0 where status = 1 and update_time < '{}' ".format(self.table, expire_time)
            result = db.do(sql)
            if result:
                print "reset:%s have count" % str(datetime.today())
            # else:
            #     print "reset:%s no count" % str(datetime.today())
            db.close()
            return result
        except Exception:
            print traceback.format_exc()
            db.close()

    def judge(self):
        if self.db is None:
            self.db = StoreMysql(**config.baidu_spider_move)

    def delete_byid(self, id, table=""):
        db = StoreMysql(**config.baidu_spider_move)
        try:
            sql = "delete from %s  where  id = %d " % (table, id)
            db.do(sql)
        except Exception, e:
            print "delete_byid exception"
            print e
        finally:
            db.close()

    def update_status_id(self, id, rank):
        db = StoreMysql(**config.baidu_spider_move)
        try:
            sql = "update task set status = 2, update_time = now(), rank={}, rank_date='{}', search_count= search_count+1 where id = {} and status < 3".format(rank, time.strftime('%Y-%m-%d', time.localtime(time.time())), id)
            print(sql)
            db.do(sql)
        except Exception, e:
            print "update_status_id exception"
            print e
        finally:
            db.close()


def Main():
    # pass
    # import config
    # sx = SourceStore(config.baidu_spider_move)
    # sx.delete_byid(607808, "task")
    rs = RankStore()
    # data = rs.find_task_lists('baidu_pc', 10)
    # for row in data:
    #     print(row)
    # rs.get_unreached_list('baidu_pc', 10)

    rs.get_yesterday_task_list('baidu_pc', 10)

if __name__ == '__main__':
    Main()
