# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     color_area_extractor
   Description :
   Author :       'li'
   date：          2020/5/9
-------------------------------------------------
   Change Activity:
                   2020/5/9:
-------------------------------------------------
"""
import cv2

from llib.cv_utility.image_opt_utility import read_image, write_image
import numpy as np


class ColorExtractor:
    def __init__(self, img=None, ):
        """
        color yellow
        """
        self.original_image = img.astype(np.float32)
        self.yellow_shreshold = 80
        pass

    def extract_color(self, color='yellow'):
        """
        extract color
        """
        if color == 'yellow':
            r, g, b = self.original_image[:, :, 0], self.original_image[:, :, 1], self.original_image[:, :, 2]
            sum_res1 = (b - r)
            sum_res2 = (g - r)
            sum_res1[np.where(sum_res1 < self.yellow_shreshold)] = 0
            sum_res1[np.where(sum_res1 >= self.yellow_shreshold)] = 1
            sum_res2[np.where(sum_res2 < self.yellow_shreshold)] = 0
            sum_res2[np.where(sum_res2 >= self.yellow_shreshold)] = 1

            sum_res = sum_res1 + sum_res2
            sum_res[np.where(sum_res < 2)] = 0
            sum_res[np.where(sum_res >= 2)] = 1
            return sum_res


def main():
    img = read_image('1.jpg')
    shape = img.shape
    # img = cv2.resize(img, (int(shape[1] / 2), int(shape[0] / 2)))
    color_extractor = ColorExtractor(img)
    res = color_extractor.extract_color()
    write_image('2.jpg', res * 255)


if __name__ == '__main__':
    main()
