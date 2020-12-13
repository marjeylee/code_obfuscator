# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     copy_file
   Description :
   Author :       'li'
   date：          2020/9/12
-------------------------------------------------
   Change Activity:
                   2020/9/12:
-------------------------------------------------
"""
import os
import shutil

from llib.file_utility.file_path_utility import get_all_files_under_directory

ORIGINAL_DIR = 'F:\内集卡\origibnal'
LINE_DIR = 'F:\内集卡\origibnal'
DELETE_DIR = 'F:\内集卡\line'
DES_DIR = 'C:/Users/lr/Desktop/新建文件夹/'


def get_name_path_mapping(dir_path):
    paths = get_all_files_under_directory(dir_path)
    mapping = {}
    for p in paths:
        _, name = os.path.split(p)
        mapping[name] = p
    return mapping


def get_delete_names():
    line_names = set(get_name_path_mapping(LINE_DIR).keys())
    delete_names = set(get_name_path_mapping(DELETE_DIR).keys())
    left_name = line_names - delete_names
    return left_name


def main():
    original_name_mapping = get_name_path_mapping(ORIGINAL_DIR)
    delete_names = get_delete_names()
    for name in delete_names:
        original_path = original_name_mapping[name]
        des_path = DES_DIR + name
        shutil.copy(original_path, des_path)
    pass


if __name__ == '__main__':
    main()
