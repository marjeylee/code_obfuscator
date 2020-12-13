# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     image_blur
   Description :
   Author :       'li'
   date：          2018/10/31
-------------------------------------------------
   Change Activity:
                   2018/10/31:
-------------------------------------------------
"""
import cv2
import numpy as np


def blur_demo(image):  # 平均模糊
    dst = cv2.blur(image, (3, 3))
    return dst


def median_blur_demo(image):  # 中值模糊
    dst = cv2.medianBlur(image, 3)
    return dst


def custom_blur_demo(image):  # 自定义卷积核
    # kernol = np.ones((5,5),np.float32)/25
    kernol = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], np.float32)  # 总和等于0或者总和等于1
    dst = cv2.filter2D(image, -1, kernol)
    return dst


def blur_image(img):
    try:
        method = np.random.choice([blur_demo, custom_blur_demo, median_blur_demo, None, None], size=1)[0]
        # print(method)
        if method is None:
            return img
        return method(img)
    except:
        return img

if __name__ == '__main__':
    im = cv2.imread('1.jpg')
    a = blur_image(im)
    pass
