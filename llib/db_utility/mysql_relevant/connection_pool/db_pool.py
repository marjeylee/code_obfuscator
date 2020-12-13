# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     db_util_pool
   Description :
   Author :       'li'
   date：          2019/9/20
-------------------------------------------------
   Change Activity:
                   2019/9/20:
-------------------------------------------------
"""
import datetime
from decimal import Decimal

import pymysql

from DBUtils.PooledDB import PooledDB

""" host=DB_IP, user=DB_USER, passwd=DB_PASSWORD,
                             db=DB_NAME, port=DB_PORT, charset='utf8'"""


class MysqlConnectionPool:

    def __init__(self, host=None, user=None, passwd=None,
                 db=None, port=None, charset='utf8'):
        self.pool = PooledDB(pymysql, 3, host=host, user=user, passwd=passwd,
                             db=db, port=int(port), charset=charset,
                             use_unicode=True, maxcached=50)

    def select(self, sql):
        """
        :param sql:
        :return:
        """
        print(sql)
        conn = self.pool.connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        columns = cursor._cursor.description
        return_result = []
        for item in result:
            obj = {}
            for index, column in enumerate(columns):
                key = column[0]
                value = item[index]
                if isinstance(value, Decimal):
                    value = float(value)
                if isinstance(value, datetime.datetime):
                    value = str(value)
                if value is None:
                    value = ''
                obj[key] = value
            return_result.append(obj)
        cursor.close()
        conn.close()
        return return_result

    def get_count(self, sql):
        """

        :param sql:
        :return:
        """
        conn = self.pool.connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return len(result)

    def execute_sql_str(self, sql):
        conn = self.pool.connection()
        cursor = conn.cursor()
        print(sql)
        try:
            cursor.execute(sql)
            conn.commit()
            return {'result': True, 'id': int(cursor.lastrowid)}
        except Exception as err:
            print(err)
            return {'result': False, 'err': err}
        finally:
            cursor.close()
            conn.close()

    def execute_sql_array(self, sqls):
        if len(sqls) == 0:
            return {'result': False}
        conn = self.__create_one_con()
        cursor = conn.cursor()
        current_sql = ''
        try:
            for sql in sqls:
                current_sql = sql
                cursor.execute(sql)
            conn.commit()
            return {'result': True, 'id': int(cursor.lastrowid)}
        except Exception as err:
            print(current_sql)
            raise err
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def __create_one_con():
        """
        get one con
        :return:
        """
        return pymysql.connect(
            host=None, user=None, password=None,
            database=None, charset='utf8')
