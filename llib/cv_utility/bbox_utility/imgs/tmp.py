# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     tmp
   Description :
   Author :       'li'
   date：          2020/6/21
-------------------------------------------------
   Change Activity:
                   2020/6/21:
-------------------------------------------------
"""
from llib.cv_utility.image_opt_utility import read_image, write_image


def main():
    mask = read_image('text.jpg') / 255
    gap = read_image('gap.jpg') / 255
    new_mask = mask * gap * 255
    write_image('new_mask.jpg', new_mask)


if __name__ == '__main__':
    main()
