# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     draw_bbox
   Description :
   Author :       'li'
   date：          2020/6/21
-------------------------------------------------
   Change Activity:
                   2020/6/21:
-------------------------------------------------
"""
import cv2
import numpy as np

from llib.cv_utility.image_opt_utility import read_image, write_image


def draw_bbox(detect_result, img):
    """
    s
    :param img:
    :param detect_result:
    :return:
    """

    for result in detect_result:
        result = np.array(result)
        result = result.astype(np.int)
        vector = np.array(result)
        vector = vector.reshape(-1, 2)
        cv2.polylines(img, [vector], isClosed=True, color=(255, 255, 0))
    return img


def draw_points(points, img):
    """

    :param points:
    :return:
    """
    for point in points:
        cv2.circle(img, tuple(point), 1, (255, 255, 0), 0)
    return img


def main():
    points = [[642, 592],
              [724, 658],
              [724, 692],
              [652, 628]]
    img = read_image('imgs/1.jpg')
    res = draw_points(points, img)
    write_image('imgs/ll.jpg', res)


if __name__ == '__main__':
    main()
