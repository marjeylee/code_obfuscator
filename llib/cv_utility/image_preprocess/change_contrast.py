# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     change_contrast
   Description :
   Author :       'li'
   date：          2018/10/31
-------------------------------------------------
   Change Activity:
                   2018/10/31:
-------------------------------------------------
"""
# -*- coding=GBK -*-
import cv2 as cv
import numpy as np

from llib.cv_utility.image_preprocess.image_blur import blur_image


def contrast_brightness_image(src1, a, g):
    h, w, ch = src1.shape  # 获取shape的数值，height和width、通道

    # 新建全零图片数组src2,将height和width，类型设置为原图片的通道类型(色素全为零，输出为全黑图片)
    src2 = np.zeros([h, w, ch], src1.dtype)
    dst = cv.addWeighted(src1, a, src2, 1 - a, g)  # addWeighted函数说明如下
    return dst


def change_contrast_and_lighten(image):
    cons = np.random.randint(80, 120, size=1)[0] / 100
    lighten = np.random.randint(-10, 10, size=1)[0]
    # print('~~~~~~~~~~~~~~~~~~~~~~~~')
    # print(cons)
    # print(lighten)
    return contrast_brightness_image(image, cons, lighten)


#
def rund():
    for i in range(1000):
        print(i)
        img = cv.imread('1.jpg')
        img = change_contrast_and_lighten(img)
        img = blur_image(img)
        cv.imwrite('-' + str(i) + '.jpg', img)
        # cv.imwrite('-111111111.jpg', img)


def change_image(img):
    try:
        img = change_contrast_and_lighten(img)
        img = blur_image(img)
        return img
    except:
        return img


if __name__ == '__main__':
    rund()
