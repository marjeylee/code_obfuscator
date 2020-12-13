# -*- coding: utf-8 -*-
"""
-------------------------------------------------
File Name： get_ip_and_mac
Description :
Author : 'li'
date： 2020/10/10
-------------------------------------------------
Change Activity:
2020/10/10:
-------------------------------------------------
"""
import os


def main():
    res = os.popen('ipconfig/all')
    print(res)
    info = res.readlines()
    lines = ''
    for line in info:
        if line == '\n':
            continue
        lines = lines + line

    print(lines)


if __name__ == '__main__':
    main()
