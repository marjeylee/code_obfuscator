# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     get_connected_domain
   Description :
   Author :       'li'
   date：          2020/5/9
-------------------------------------------------
   Change Activity:
                   2020/5/9:
-------------------------------------------------
"""
import cv2
import numpy as np

from llib.cv_utility.image_opt_utility import read_image, write_image


def get_connected_domains_list(format_pixel):
    """
    combine and return connected domains
    :param format_pixel:
    :return:
    """
    _, labels = cv2.connectedComponents(format_pixel.astype(np.uint8))
    max_label = labels.max() + 1
    connected_domains = []
    for i in range(1, max_label):
        domain = np.zeros_like(labels)
        domain[np.where(labels == i)] = 1
        connected_domains.append(domain)
    return connected_domains


def main():
    img = read_image('2.jpg') / 255
    img[np.where(img > 0.6)] = 1
    img[np.where(img <= 0.6)] = 0
    connected_domains = get_connected_domains_list(img)
    for index, domain in enumerate(connected_domains):
        write_image('cont' + str(index) + '.jpg', domain * 255)


if __name__ == '__main__':
    main()
