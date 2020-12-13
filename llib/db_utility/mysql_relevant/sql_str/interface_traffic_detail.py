# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     interface_traffic_detail
   Description :
   Author :       'li'
   date：          2020/3/23
-------------------------------------------------
   Change Activity:
                   2020/3/23:
-------------------------------------------------
"""
INSERT_INTERFACE_TRAFFIC_DETAIL = """
INSERT INTO `interface_traffic_detail` (
  `id`,
  `ip`,
  `traffic_info`,
  `check_time`
) 
VALUES
  ('%s', '%s', '%s', '%s') ;"""
QUERY_INTERFACE_TRAFFIC_DETAIL = """
SELECT 
  * 
FROM
  `interface_traffic_detail` AS a WHERE 1=1 """
