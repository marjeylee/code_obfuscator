# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     file_io_utility
   Description :
   Author :       'li'
   date：          2018/8/3
-------------------------------------------------
   Change Activity:
                   2018/8/3:
-------------------------------------------------
"""
import hashlib
import os


def read_all_content(file_path, encoding='utf8'):
    """
    read files content
    :param file_path:
    :param encoding:
    :return:
    """
    with open(file_path, mode='r', encoding=encoding) as file:
        lines = file.readlines()
        content = ''
        for line in lines:
            content = content + line
        return content


def get_file_md5(filename):
    if not os.path.isfile(filename):
        return
    my_hash = hashlib.md5()
    f = open(filename, 'rb')
    while True:
        b = f.read(8096)
        if not b:
            break
        my_hash.update(b)
    f.close()
    return str(my_hash.hexdigest())


def read_lines(p,encoding='utf8'):
    """return the text in a file in lines as a list """
    f = open(p, 'r', encoding=encoding)
    return f.readlines()
