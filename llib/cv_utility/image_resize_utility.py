# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     image_resize
   Description :
   Author :       'li'
   date：          2020/3/31
-------------------------------------------------
   Change Activity:
                   2020/3/31:
-------------------------------------------------
"""
import cv2
import numpy as np

from llib.random_utility.random_utility import get_random_int


class ImageUtility:
    @staticmethod
    def random_resize(img, height_range=(0.8, 1.2), wight_range=(0.8, 1.2)):
        """
        resize
        """
        shape = img.shape
        new_height = get_random_int(height_range[0] * 100, height_range[1] * 100) / 100 * shape[0]
        new_wight = get_random_int(wight_range[0] * 100, wight_range[1] * 100) / 100 * shape[1]
        resize_image = cv2.resize(img, (int(new_wight), int(new_height)))
        return resize_image

    @staticmethod
    def resize_to_fix_height(img, fix_height=32, max_width=320):
        """
        resize
        :param max_width:
        :param img:
        :param fix_height:
        :return:
        """
        shape = img.shape
        ratio = shape[0] / fix_height
        resize_image = cv2.resize(img, (min(int(shape[1] / ratio), max_width), fix_height))
        return resize_image

    @staticmethod
    def resize_to_fix_width(img, fix_width=32, max_height=320):
        """

        :param max_height:
        :param img:
        :param fix_width:
        :return:
        """
        shape = img.shape
        ratio = shape[1] / fix_width
        resize_image = cv2.resize(img, (fix_width, min(int(shape[0] / ratio), max_height)))
        return resize_image

    @staticmethod
    def img_zero_padding(img, des_height, des_width):
        """
        img zero padding
        :param img:
        :param des_height:
        :param des_width:
        :return:
        """
        if len(img.shape) == 3:
            h, w, c = img.shape
            dtype = img.dtype
            bg = np.zeros(shape=(des_height, des_width, c), dtype=dtype)
            bg[0:h, 0:w, :] = img
            return bg
        else:
            h, w = img.shape
            dtype = img.dtype
            bg = np.zeros(shape=(des_height, des_width), dtype=dtype)
            bg[0:h, 0:w] = img
            return bg

    @staticmethod
    def horizontal_splicing_picture(img1, img2, height=32):
        """
        水平拼接两张图片
        :param img1:
        :param img2:
        :return:
        """
        shape1 = img1.shape
        radio1 = shape1[0] / height
        shape2 = img2.shape
        radio2 = shape2[0] / height
        img1 = cv2.resize(img1, (int(shape1[1] / radio1), height))
        img2 = cv2.resize(img2, (int(shape2[1] / radio2), height))
        return np.concatenate((img1, img2), axis=1)

    @staticmethod
    def vertical_splicing_picture(img1, img2):
        """
        水平拼接两张图片
        :param img1:
        :param img2:
        :return:
        """
        shape1 = img1.shape
        radio1 = shape1[1] / 32
        shape2 = img2.shape
        radio2 = shape2[1] / 32
        img1 = cv2.resize(img1, (32, int(shape1[0] / radio1)))
        img2 = cv2.resize(img2, (32, int(shape2[0] / radio2)))
        return np.concatenate((img1, img2), axis=0)
