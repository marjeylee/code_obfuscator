# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     labelme_json_to_nyp_training_data
   Description :
   Author :       'li'
   date：          2020/11/18
-------------------------------------------------
   Change Activity:
                   2020/11/18:
-------------------------------------------------
"""
import base64
import json
import os

import cv2
import numpy as np

from config.detection_config import JSON_DIR, NPY_DIR
from llib.cv_utility.image_opt_utility import read_image, write_image, enlarge_bbox
from llib.file_utility.file_io_utility import read_all_content
from llib.file_utility.file_path_utility import get_all_file_from_dir

JSON_PATH = JSON_DIR
DES_NPY_PATH = NPY_DIR
ENLARGE_RATIO = 1
IS_CLIP_IMAGE = True
TEXTAREA_REDUCTION_SCALE = 2
GAP_ENLARGE_RATIO = 3


def get_image(img_str):
    """

    """
    fh = open('tmp.jpg', "wb")
    fh.write(base64.b64decode(img_str))
    fh.close()
    img = read_image('tmp.jpg')
    shape = img.shape
    img = cv2.resize(img, (int(shape[1] * ENLARGE_RATIO), int(shape[0] * ENLARGE_RATIO)))
    return img


def get_textarea_mask(shapes, img):
    img_shape = img.shape
    map_score = np.zeros(
        shape=(int(img_shape[0] / TEXTAREA_REDUCTION_SCALE), int(img_shape[1] / TEXTAREA_REDUCTION_SCALE)))
    for shape in shapes:
        points = shape['points']
        points = np.array(points)
        points = points.reshape((-1, 2)).astype(np.int) // TEXTAREA_REDUCTION_SCALE
        map_score = cv2.drawContours(map_score, [points], -1, 1, -1)
    return map_score


def get_gap_mask(shapes, img):
    img_shape = img.shape
    map_score = np.zeros(shape=(int(img_shape[0] / TEXTAREA_REDUCTION_SCALE),
                                int(img_shape[1] / TEXTAREA_REDUCTION_SCALE)))
    for shape in shapes:
        points = shape['points']
        if len(points) != 4:
            return None
        tmp_mask = np.zeros(shape=(int(img_shape[0] / TEXTAREA_REDUCTION_SCALE),
                                   int(img_shape[1] / TEXTAREA_REDUCTION_SCALE)))
        points = np.array(points)
        points = points.reshape((-1, 2)).astype(np.int) // TEXTAREA_REDUCTION_SCALE
        tmp_mask = cv2.drawContours(tmp_mask, [points], -1, 1, -1)
        gap_mask = np.zeros(shape=(int(img_shape[0] / TEXTAREA_REDUCTION_SCALE),
                                   int(img_shape[1] / TEXTAREA_REDUCTION_SCALE)))
        enlarge_point = enlarge_bbox(GAP_ENLARGE_RATIO, points, img_shape)
        enlarge_point = np.array(enlarge_point)
        gap_mask = cv2.drawContours(gap_mask, [enlarge_point], -1, 1, -1)
        gap_mask = gap_mask - tmp_mask
        map_score = map_score + gap_mask
    map_score[np.where(map_score > 1)] = 1
    return map_score


def _main():
    paths = get_all_file_from_dir(JSON_PATH)
    # try:
    for i, p in enumerate(paths):
        if '.json' not in p:
            continue
        print(i)
        if i < 0:
            continue
        try:
            content = read_all_content(p, 'gbk')
            obj = json.loads(content)
            file_name = os.path.split(p)[1].split('.')[0]
            img = get_image(obj['imageData'])
            textarea_mask = get_textarea_mask(obj['shapes'], img)
            gap_mask = get_gap_mask(obj['shapes'], img)
            # write_image('img.jpg', img * 255)
            # write_image('text.jpg', textarea_mask * 255)
            # write_image('gap.jpg', gap_mask * 255)

            np.save(DES_NPY_PATH + file_name + '.npy', [img, textarea_mask, gap_mask])
        except Exception as e:
            print(e)
            pass


if __name__ == '__main__':
    _main()
