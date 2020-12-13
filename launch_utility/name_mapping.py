# -*- coding: utf-8 -*-
"""
-------------------------------------------------
File Name： name_mapping
Description :
Author : 'li'
date： 2020/12/9
-------------------------------------------------
Change Activity:
2020/12/9:
-------------------------------------------------
"""
from llib.random_utility.uuid_utility import get_uuid_str


class NameMapping:
    def __init__(self, names):
        self.names = names
        self.name_str_mapping = {}
        self.str_name_mapping = {}
        self._load_mapping()

    def _load_mapping(self):
        self.names.add('self')
        for name in self.names:
            random_str = 'l' + get_uuid_str()
            self.name_str_mapping[name] = random_str
            self.str_name_mapping[random_str] = name
