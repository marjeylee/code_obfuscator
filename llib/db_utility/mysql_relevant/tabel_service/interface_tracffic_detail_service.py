# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     interface_tracffic_detail_service
   Description :
   Author :       'li'
   date：          2020/3/23
-------------------------------------------------
   Change Activity:
                   2020/3/23:
-------------------------------------------------
"""
import time

from lib.common.utility.uuid_utility import get_uuid_str
from lib.db.mysql_relevant.connection_pool.db_pool import DB_POOL
from lib.db.mysql_relevant.sql_str.interface_traffic_detail import *
from lib.db.mysql_relevant.util.sql_parameter_type_change import TypeChange


class InterfaceTrafficDetail:
    @staticmethod
    def insert_obj(obj):
        check_time = time.time()
        check_time = TypeChange.date_stamp_to_datetime(check_time)
        sql = INSERT_INTERFACE_TRAFFIC_DETAIL % (get_uuid_str(),
                                                 TypeChange.to_string(obj, 'ip'),
                                                 TypeChange.to_string(obj, 'traffic_info'),
                                                 check_time)
        DB_POOL.execute_sql_str(sql)

    @staticmethod
    def query_info(ip, start_time, end_time):
        """
            2020-04-01 19:39:54
        :param ip:
        :param start_time:
        :param end_time:
        :return:
        """
        sql = QUERY_INTERFACE_TRAFFIC_DETAIL + """AND `ip` = '%s'  AND `check_time` >'%s'""" % (ip, start_time)
        if end_time is not None:
            sql = sql + "and `check_time`<'$s'" % end_time
        sql = sql + """order by check_time ; """
        return DB_POOL.select(sql)


def main():
    obj = {'ip': '123', "traffic_info": 'dsada'}
    res = InterfaceTrafficDetail.query_info('10.5.1.118', '2020-03-06 05:31:15', None)
    print(res)


if __name__ == '__main__':
    main()
