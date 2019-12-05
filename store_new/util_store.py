# -*- coding: utf8 -*-
import os
import sys

import MySQLdb
import traceback

# from download_center.store.store_mysql_pool import StoreMysqlPool

from store_new.store_mysql_pool import StoreMysqlPool

reload(sys)
sys.setdefaultencoding('utf8')


class SourceStore(object):

    def __init__(self, db_conn):
        # 数据库连接信息
        self.db = StoreMysqlPool(**db_conn)

    def insert_row(self, sql, flag='rowcount'):
        return self.db.do(sql, flag)

    def store_table(self, results, table="", type=1, field=None):
        try:
            if len(results) > 0:
                for result in results:
                    if type == 1:
                        for key in result:
                            result[key] = MySQLdb.escape_string(
                                str(result[key]))
                        return_state = self.db.save(table, result)
                    elif type == 2:
                        for key in result:
                            result[key] = MySQLdb.escape_string(
                                str(result[key]))
                        return_state = self.db.update(table, result, field)
                return return_state
        except Exception:
            print(traceback.format_exc())
            return -1

    def store_table_one(self, result, table="", type=1, field=None):
        """
        单个  保存或更新
        :param result: 记录<dict>
        :param table:  表名字
        :param type:   1:保存 2:更新
        :param field:  字段名
        :return: 状态
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
                            result[key] = MySQLdb.escape_string(
                                str(result[key]))
                        return_state = self.db.save(table, result)
                    elif type == 2:
                        for key in result:
                            result[key] = MySQLdb.escape_string(
                                str(result[key]))
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
            store_id = 0
            if len(results) > 0:
                for result in results:
                    # values = ''
                    field_value = None
                    for key in result:
                        result[key] = MySQLdb.escape_string(str(result[key]))
                        if key == field:
                            field_value = result[key]
                        # values += "%s='%s'," % (str(key), str(result[key]))
                    if field:
                        field_result = self.find_by_field(
                            table, field, field_value)
                        if field_result:
                            if isupdate == 1:
                                self.db.update(table, result, field)
                            else:
                                pass
                        else:
                            store_id = self.db.save(table, result)
                    else:
                        store_id = self.db.save(table, result)
                return store_id
        except Exception:
            print(traceback.format_exc())
            return -1

    def find_all(self, table_name):
        try:
            sql = "select * from %s " % (
                table_name)
            result = self.db.query(sql)
            return result
        except Exception:
            print traceback.format_exc()

    def exq_sql(self, sql):
        """
        直接执行sql语句
        """
        try:
            result = self.db.query(sql)
            return result
        except Exception:
            print traceback.format_exc()

    def find_by_field(self, table_name, field, field_value):
        try:
            sql = "select * from %s where %s = '%s' " % (
                table_name, field, field_value)
            result = self.db.query(sql)
            return result
        except Exception:
            print traceback.format_exc()

    def find_by_fields(self, table, queryset={}):
        """
        从数据库里查询 符合多个条件的记录 
        Args:
            table: 表名字 str
            queryset : key 字段 value 值 dict
        return:
            成功： [dict] 保存的记录
            失败： -1
        """
        try:
            querrys = ""
            for k, v in queryset.items():
                querrys += "{} = '{}' and ".format(k, v)
            sql = "select * from {} where {} ".format(
                table, querrys[:-4])
            result = self.db.query(sql)
            return result
        except:
            print(traceback.format_exc())
            return -1

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
                sql = "delete from %s  where  id = %d " % (
                    table, single_id['id'])
                self.db.query(sql)
            except Exception, e:
                print e
                pass

if __name__ == '__main__':
    import config
    s = SourceStore(config.game_spiders)

    # from download_center.store.store_mysql_pool import StoreMysqlPool
    # s = StoreMysqlPool(**config.weixin_content)

    sql = "insert ignore into game_gl_message(md5, type) values('12', '1')"
    print s.insert_row(sql, 'rowcount')