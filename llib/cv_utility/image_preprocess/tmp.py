# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     tmp
   Description :
   Author :       'li'
   date：          2020/8/11
-------------------------------------------------
   Change Activity:
                   2020/8/11:
-------------------------------------------------
"""
import numpy as np
import cv2

from llib.cv_utility.image_opt_utility import write_image

file_name = "1.jpg"
img = cv2.imread(file_name)

# gray = np.float32(gray)
# rocg = Recognise.Recognise()
image = np.power(img / 255.0, 0.7)
# image = rocg.gamma_rectify(gray, 0.4)
write_image('33.jpg', image * 255)
