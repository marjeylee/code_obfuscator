# -*- coding: utf-8 -*-
"""
-------------------------------------------------
File Name： __init__.py
Description :
Author : 'li'
date： 2020/12/8
-------------------------------------------------
Change Activity:
2020/12/8:
-------------------------------------------------
"""
import json


class dsa:
    @staticmethod
    def asd(a):
        return json.dumps(a)


c = getattr(dsa, 'asd')({'a': 1})
print(c)
