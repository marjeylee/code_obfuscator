# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     enlighten_image_np
   Description :
   Author :       'li'
   date：          2020/7/25
-------------------------------------------------
   Change Activity:
                   2020/7/25:
-------------------------------------------------
"""
import os

import cv2

from llib.cv_utility.image_opt_utility import read_image, to_gray, write_image
import numpy as np

from llib.file_utility.file_path_utility import get_all_files_under_directory


def enlighten_image_np(des_mean_value, img):
    """
    :param des_mean_value:
    :param img:
    :return:
    """
    if len(img.shape) != 2:
        gray_image = to_gray(img)
    else:
        gray_image = img
    mean_value = gray_image.mean()
    ratio = mean_value / des_mean_value
    img = img / 255
    new_image = np.power(img, ratio)
    new_image = new_image * 255
    new_mean_value = new_image.mean()
    return new_image


def lpls_enlighten(img):
    kernel = np.array([[0, -1, 0], [0, 5, 0], [0, -1, 0]])  # 定义卷积核
    image_enhance = cv2.filter2D(img, -1, kernel)  # 进行卷积运算
    return image_enhance


def main():
    # img = to_gray(img)
    # mean_value = img.mean()
    # print(mean_value)

    # paths = get_all_files_under_directory('E:/qianfen_area')
    # for path in paths:
    #     img = read_image(path)
    #     img = enlighten_image_np(111, img)
    #     _, name = os.path.split(path)
    #     write_image('E:/new_area/' + name, img)
    """"""
    img = read_image('1.jpg')

    img = lpls_enlighten(img)
    write_image('2.jpg', img)


if __name__ == '__main__':
    main()
