# -*- coding: utf8 -*-
import os
import sys
import config
import MySQLdb
import traceback

from download_center.store.store_mysql_pool import StoreMysqlPool

reload(sys)
sys.setdefaultencoding('utf8')


class SourceStore(object):

    def __init__(self, db_conn):
        # 数据库连接信息
        # print("SourceStore init db")
        self.db = StoreMysqlPool(**db_conn)

    def store_table(self, results, table="", type=1, field=None):
        try:
            if len(results) > 0:
                for result in results:
                    if type == 1:
                        for key in result:
                            result[key] = MySQLdb.escape_string(str(result[key]))
                        return_state = self.db.save(table, result)
                    elif type == 2:
                        for key in result:
                            result[key] = MySQLdb.escape_string(str(result[key]))
                        return_state = self.db.update(table, result, field)
                return return_state
        except Exception:
            print(traceback.format_exc())
            return -1

    def store_table_one(self, result, table="", type=1, field=None):
        """
        单个  保存或更新
        :param result:
        :param table:
        :param type:
        :param field:
        :return:
        """
        try:
            if type == 1:
                for key in result:
                    result[key] = MySQLdb.escape_string(str(result[key]))
                return_state = self.db.save(table, result)
            elif type == 2:
                for key in result:
                    result[key] = MySQLdb.escape_string(str(result[key]))
                return_state = self.db.update(table, result, field)
            return return_state
        except Exception:
            print(traceback.format_exc())
            return -1

    def store_table_db(self, results, table="", type=1, field=None):
        return_state = 0
        if len(results) > 0:
            for result in results:
                try:
                    if type == 1:
                        for key in result:
                            result[key] = MySQLdb.escape_string(str(result[key]))
                        return_state = self.db.save(table, result)
                    elif type == 2:
                        for key in result:
                            result[key] = MySQLdb.escape_string(str(result[key]))
                        return_state = self.db.update(table, result, field)
                except:
                    print(traceback.format_exc())
                    return -1
            return return_state

    def saveorupdate(self, results, table="", field=None):
        try:
            if len(results) > 0:
                for result in results:
                    for key in result:
                        result[key] = MySQLdb.escape_string(str(result[key]))
                    return_state = self.db.saveorupdate(table, result, field)
                return return_state
        except Exception:
            print(traceback.format_exc())
            return -1

    def store_insert_or_update(self, results, table="", field=None, isupdate=1):
        """
        isupdate == 1 更新  2： pass  不传field 直接保存  saveorupdate
        :param results:
        :param table:
        :param field:
        :param isupdate:
        :return:
        """
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
                                self.db.update(table, result, field)
                            else:
                                pass
                        else:
                            self.db.save(table, result)
                    else:
                        self.db.save(table, result)
        except Exception:
            print(traceback.format_exc())
            return -1

    def find_by_field(self, table_name, field, field_value):
        try:
            sql = "select * from %s where %s = %s " % (table_name, field, field_value)
            result = self.db.query(sql)
            self.db.close()
            return result
        except Exception:
            print traceback.format_exc()

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
        for single_id in ids:
            try:
                sql = "delete from %s  where  id = %d " % (table, single_id['id'])
                self.db.query(sql)
            except Exception, e:
                print e
                pass

    def delete_byid(self, id, table=""):
        try:
            sql = "delete from %s  where  id = %d " % (table, id)
            self.db.do(sql)
        except Exception, e:
            print "delete_byid exception"
            print e

    def update_status_id(self, id, table=""):
        try:
            sql = "update {} set status = 2, update_time = now() where id = {}".format(table, id)
            self.db.do(sql)
        except Exception, e:
            print "update_status_id exception"
            print e


def test():
    import config
    sx = SourceStore(config.baidu_spider_move)
    sx.delete_byid(607808, "task")

if __name__ == '__main__':
    test()
