# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     image_opt_utility
   Description :
   Author :       'li'
   date：          2020/4/1
-------------------------------------------------
   Change Activity:
                   2020/4/1:
-------------------------------------------------
"""
import cv2
import numpy as np


def to_gray(copy_img):
    """
    image to gray
    :param copy_img:
    :return:
    """
    return cv2.cvtColor(copy_img, cv2.COLOR_BGR2GRAY)


def enlarge_bbox(enlarge_pixel, bbox, shape):
    """
    enlarge bbox
    :param enlarge_pixel:
    :param shape:
    :param bbox:
    :return:
    """
    p1, p2, p3, p4 = bbox[0], bbox[1], bbox[2], bbox[3]
    p1 = [p1[0] - enlarge_pixel, p1[1] - enlarge_pixel]
    p2 = [p2[0] + enlarge_pixel, p2[1] - enlarge_pixel]
    p3 = [p3[0] + enlarge_pixel, p3[1] + enlarge_pixel]
    p4 = [p4[0] - enlarge_pixel, p4[1] + enlarge_pixel]
    bbox = [p1, p2, p3, p4]
    img_height, img_width = shape[0], shape[1]
    for point in bbox:
        width, height = point
        if width < 0:
            point[0] = 0
        if height < 0:
            point[1] = 0
        if height > img_height:
            point[1] = img_height
        if width > img_width:
            point[0] = img_width
    return bbox


def enlarge_vertical_bbox(enlarge_pixel, bbox, shape):
    """
    enlarge bbox (width,height)
    :param enlarge_pixel:
    :param shape:
    :param bbox:
    :return:
    """
    p1, p2, p3, p4 = bbox[0], bbox[1], bbox[2], bbox[3]
    p1 = [p1[0], p1[1] - enlarge_pixel]
    p2 = [p2[0], p2[1] - enlarge_pixel]
    p3 = [p3[0], p3[1] + enlarge_pixel]
    p4 = [p4[0], p4[1] + enlarge_pixel]
    bbox = [p1, p2, p3, p4]
    img_height, img_width, _ = shape
    for point in bbox:
        width, height = point
        if width < 0:
            point[0] = 0
        if height < 0:
            point[1] = 0
        if height > img_height:
            point[1] = img_height
        if width > img_width:
            point[0] = img_width
    return bbox


def read_image(image_path):
    """
    handle chinese char in path
    :param image_path:
    :return:
    """
    img = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), -1)
    return img


def write_image(img_path, img):
    """

    :param img_path:
    :param img:
    :return:
    """
    cv2.imencode('.jpg', img)[1].tofile(img_path)


def rotate_image(image, angle, center=None, scale=1.0):
    """
    rotate image
    """
    (h, w) = image.shape[:2]
    if center is None:
        center = (w / 2, h / 2)
    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(image, M, (h, w))
    return rotated


def main():
    img = read_image('1.jpg')
    img = np.rot90(img)
    img = np.rot90(img)
    img = np.rot90(img)
    write_image('2.jpg', img)


if __name__ == '__main__':
    main()
