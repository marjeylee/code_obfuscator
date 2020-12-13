# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     random_utility
   Description :
   Author :       'li'
   date：          2020/3/30
-------------------------------------------------
   Change Activity:
                   2020/3/30:
-------------------------------------------------
"""
import random

import numpy as np


def fetch_item_from_list(list_info, size):
    """
    fetch_item from list
    :param list_info:
    :param size:
    :return:
    """
    return np.random.choice(list_info, size).tolist()


def get_random_int(start, end):
    """
    get random int
    :param start:
    :param end:
    :return:
    """
    return random.randrange(start, end)


def get_random_true_or_false(true_ratio=0.5):
    """

    :param true_ratio:
    :return:
    """
    boolean_value = True if random.random() < true_ratio else False
    return boolean_value


if __name__ == '__main__':
    for i in range(100):
        print(get_random_true_or_false(0.5))
