# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     composize_image
   Description :
   Author :       'li'
   date：          2020/8/15
-------------------------------------------------
   Change Activity:
                   2020/8/15:
-------------------------------------------------
"""
import os

from llib.cv_utility.image_opt_utility import read_image, write_image
from llib.cv_utility.image_preprocess.jittering_methods import *
from llib.cv_utility.image_resize_utility import ImageUtility
from llib.file_utility.file_path_utility import combine_file_path, get_all_files_under_directory
import numpy as np

from llib.random_utility.random_utility import fetch_item_from_list

CHAR_DIR = combine_file_path('resource/char')


def __load_char_mapping():
    """

    """
    char_mapping = {}
    char_paths = get_all_files_under_directory(CHAR_DIR)
    for p in char_paths:
        _, name = os.path.split(p)
        label = name.split('_')[0]
        img = read_image(p)
        if label not in char_mapping:
            char_mapping[label] = []
        char_mapping[label] = img
    return char_mapping


CHAR_IMAGE_MAPPING = __load_char_mapping()


def composite_image(words):
    """

    """
    bg = None
    for char in words:
        img = CHAR_IMAGE_MAPPING[char]
        img = ImageUtility.resize_to_fix_height(img, 32)
        if bg is None:
            bg = img
        else:
            bg = np.concatenate([bg, img], axis=1)
    return bg


def gen_random_words(batch_size=10):
    training_data = []
    for _ in range(batch_size):
        words_template = list('QWERTYUIOPASDFGHJKLZXCVBNM0123456789')
        for char_size in [3, 4, 5]:
            chars = fetch_item_from_list(words_template, char_size)
            words = ''.join(chars)
            img = composite_image(words)
            img = ImageUtility.random_resize(img, height_range=(1, 1.2), wight_range=(0.6, 1))
            img = jittering_all(img)
            training_data.append([img, words])
    return training_data


def main():
    training_data = gen_random_words()
    for img, label in training_data:
        write_image(label + '.jpg', img)


if __name__ == '__main__':
    main()
