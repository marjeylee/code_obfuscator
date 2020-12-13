# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     composite_image_from_char
   Description :
   Author :       'li'
   date：          2020/8/15
-------------------------------------------------
   Change Activity:
                   2020/8/15:
-------------------------------------------------
"""
from llib.cv_utility.image_opt_utility import write_image
from llib.file_utility.file_path_utility import combine_file_path, get_all_files_under_directory
from PIL import Image, ImageDraw, ImageFont

from llib.random_utility.random_utility import fetch_item_from_list
import numpy as np

from llib.random_utility.uuid_utility import get_uuid_str

TTF_PATHS = get_all_files_under_directory(combine_file_path('resource/font'))
FONT_SIZE = 44


def __load_font_objects():
    font_lst = []
    for path in TTF_PATHS:
        font = ImageFont.truetype(path, FONT_SIZE)
        font_lst.append(font)
    return font_lst


FONT_OBJECTS = __load_font_objects()


def char_to_image(char):
    """
    char
    """
    des_dir = combine_file_path('resource/char') + '/'
    for font in FONT_OBJECTS:
        size = font.getsize(char)
        scene_text = Image.new('RGBA', size)
        draw = ImageDraw.Draw(scene_text)
        draw.text((0, 0), char, font=font)
        scene_text = np.array(scene_text)
        start_index = 0
        for i in range(30):
            if scene_text[i, :, :].max() == 0:
                start_index = i
            else:
                break
        new_area = scene_text[start_index:, :, :]
        write_image(des_dir + char + '_' + get_uuid_str() + '.jpg', 255 - new_area)


def main():
    words = 'QWERTYUIOPASDFGHJKLZXCVBNM0123456789'
    for char in words:
        char_to_image(char)


if __name__ == '__main__':
    main()
