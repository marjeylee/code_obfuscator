# -*- coding: utf-8 -*-
"""
-------------------------------------------------
File Name： config
Description :
Author : 'li'
date： 2020/11/12
-------------------------------------------------
Change Activity:
2020/11/12:
-------------------------------------------------
"""
from llib.file_utility.file_path_utility import combine_file_path
import yaml


class YAMLConfiguration:
    def __init__(self):
        self.config = self.__load_config_from_yml_file(combine_file_path('config/config.yml'))

    @staticmethod
    def __load_config_from_yml_file(yml_path):
        with open(yml_path, mode='r', encoding='utf8') as file:
            content = file.read()
            yml_content = yaml.load(content, yaml.FullLoader)
            return yml_content

    def fetch_value(self, key_lst):
        tmp_value = self.config
        for key in key_lst:
            tmp_value = tmp_value[key]
        return tmp_value

    def reload_config(self):
        self.config = self.__load_config_from_yml_file(combine_file_path('config/config.yml'))


CONFIGURATION = YAMLConfiguration()


def _main():
    YAMLConfiguration()


if __name__ == '__main__':
    _main()
