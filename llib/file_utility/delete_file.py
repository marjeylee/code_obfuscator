# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     delete_file
   Description :
   Author :       'li'
   date：          2018/8/19
-------------------------------------------------
   Change Activity:
                   2018/8/19:
-------------------------------------------------
"""
import os
import shutil


def main():
    for i in range(100):
        try:
            dir_path = 'D:/网络规划设计师'
            shutil.rmtree(dir_path)
            os.mkdir(dir_path)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()
