# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     v3_utility
   Description :
   Author :       'li'
   date：          2020/8/7
-------------------------------------------------
   Change Activity:
                   2020/8/7:
-------------------------------------------------
"""
import copy
import numpy as np

from llib.cv_utility.bbox_utility.draw_line_from_point import translation_line_first_side, draw_line_from_points, \
    translation_line_second_side, translation_line
from llib.cv_utility.image_opt_utility import write_image


def _sort_location(location):
    """

    """
    points_size = location[0].size
    first_location = [2000, 2000]
    last_location = [0, 0]
    for i in range(points_size):
        width = location[1][i]
        if first_location[0] > width:
            first_location = location[1][i], location[0][i]
        if last_location[0] < width:
            last_location = location[1][i], location[0][i]
    return first_location, last_location


def approaching_horizontal_point0(bg, line1):
    """

    """
    center_point = (line1[0][0] + line1[1][0]) / 2 - 5, (line1[0][1] + line1[1][1]) / 2
    pt1, pt2 = line1
    original_pt1, original_pt2 = copy.deepcopy(pt1), copy.deepcopy(pt2)
    original_pt1 = original_pt1[0] - 2, original_pt1[1]
    original_pt2 = original_pt2[0] - 2, original_pt2[1]
    pt1, pt2 = original_pt1, center_point
    while True:
        pt1, pt2 = translation_line_first_side(pt1, pt2, direction='right')
        tmp_bg = np.zeros_like(bg)
        tmp_bg = draw_line_from_points([pt1, pt2], tmp_bg, line_pixel=1)
        tmp_bg = tmp_bg + bg
        write_image('tmp_bg.jpg', tmp_bg * 255)
        max_value = np.max(tmp_bg)
        if max_value > 1:
            location = np.where(tmp_bg > 1)
            first_location, last_location = _sort_location(location)
            first_point = first_location
            break
    pt1, pt2 = center_point, original_pt2
    while True:
        pt1, pt2 = translation_line_second_side(pt1, pt2, direction='right')
        tmp_bg = np.zeros_like(bg)
        tmp_bg = draw_line_from_points([pt1, pt2], tmp_bg, line_pixel=1)
        tmp_bg = tmp_bg + bg
        write_image('tmp_bg.jpg', tmp_bg * 255)
        max_value = np.max(tmp_bg)
        if max_value > 1:
            location = np.where(tmp_bg > 1)
            first_location, last_location = _sort_location(location)
            second_point = first_location
            break
    pt1, pt2 = first_point, second_point
    while True:
        pt1, pt2 = translation_line(pt1, pt2, direction='left')
        tmp_bg = np.zeros_like(bg)
        tmp_bg = draw_line_from_points([pt1, pt2], tmp_bg, line_pixel=1)
        tmp_bg = tmp_bg + bg
        write_image('tmp_bg.jpg', tmp_bg * 255)
        max_value = np.max(tmp_bg)
        if max_value <= 1:
            return pt1, pt2


def approaching_horizontal_point2(bg, line1):
    """

    """
    center_point = (line1[0][0] + line1[1][0]) / 2 + 5, (line1[0][1] + line1[1][1]) / 2
    pt1, pt2 = line1
    original_pt1, original_pt2 = copy.deepcopy(pt1), copy.deepcopy(pt2)
    original_pt1 = original_pt1[0] + 2, original_pt1[1]
    original_pt2 = original_pt2[0] + 2, original_pt2[1]
    pt1, pt2 = original_pt1, center_point
    while True:
        pt1, pt2 = translation_line_first_side(pt1, pt2, direction='left')
        tmp_bg = np.zeros_like(bg)
        tmp_bg = draw_line_from_points([pt1, pt2], tmp_bg, line_pixel=1)
        tmp_bg = tmp_bg + bg
        write_image('tmp_bg.jpg', tmp_bg * 255)
        max_value = np.max(tmp_bg)
        if max_value > 1:
            location = np.where(tmp_bg > 1)
            first_location, last_location = _sort_location(location)
            first_point = first_location
            break
    pt1, pt2 = center_point, original_pt2
    while True:
        pt1, pt2 = translation_line_second_side(pt1, pt2, direction='left')
        tmp_bg = np.zeros_like(bg)
        tmp_bg = draw_line_from_points([pt1, pt2], tmp_bg, line_pixel=1)
        tmp_bg = tmp_bg + bg
        write_image('tmp_bg.jpg', tmp_bg * 255)
        max_value = np.max(tmp_bg)
        if max_value > 1:
            location = np.where(tmp_bg > 1)
            first_location, last_location = _sort_location(location)
            second_point = first_location
            break
    pt1, pt2 = first_point, second_point
    while True:
        pt1, pt2 = translation_line(pt1, pt2, direction='right')
        tmp_bg = np.zeros_like(bg)
        tmp_bg = draw_line_from_points([pt1, pt2], tmp_bg, line_pixel=1)
        tmp_bg = tmp_bg + bg
        write_image('tmp_bg.jpg', tmp_bg * 255)
        max_value = np.max(tmp_bg)
        if max_value <= 1:
            return pt1, pt2


def approaching_vertical_point0(bg, line1):
    """

    """
    center_point = (line1[0][0] + line1[1][0]) / 2, (line1[0][1] + line1[1][1]) / 2 - 5
    pt1, pt2 = line1
    original_pt1, original_pt2 = copy.deepcopy(pt1), copy.deepcopy(pt2)
    original_pt1 = original_pt1[0], original_pt1[1] - 2
    original_pt2 = original_pt2[0], original_pt2[1] - 2
    pt1, pt2 = original_pt1, center_point
    while True:
        pt1, pt2 = translation_line_first_side(pt1, pt2, direction='down')
        tmp_bg = np.zeros_like(bg)
        tmp_bg = draw_line_from_points([pt1, pt2], tmp_bg, line_pixel=1)
        tmp_bg = tmp_bg + bg
        write_image('tmp_bg.jpg', tmp_bg * 255)
        max_value = np.max(tmp_bg)
        if max_value > 1:
            location = np.where(tmp_bg > 1)
            first_location, last_location = _sort_location(location)
            first_point = first_location
            break
    pt1, pt2 = center_point, original_pt2
    while True:
        pt1, pt2 = translation_line_second_side(pt1, pt2, direction='down')
        tmp_bg = np.zeros_like(bg)
        tmp_bg = draw_line_from_points([pt1, pt2], tmp_bg, line_pixel=1)
        tmp_bg = tmp_bg + bg
        write_image('tmp_bg.jpg', tmp_bg * 255)
        max_value = np.max(tmp_bg)
        if max_value > 1:
            location = np.where(tmp_bg > 1)
            first_location, last_location = _sort_location(location)
            second_point = first_location
            break
    pt1, pt2 = first_point, second_point
    while True:
        pt1, pt2 = translation_line(pt1, pt2, direction='up')
        tmp_bg = np.zeros_like(bg)
        tmp_bg = draw_line_from_points([pt1, pt2], tmp_bg, line_pixel=1)
        tmp_bg = tmp_bg + bg
        write_image('tmp_bg.jpg', tmp_bg * 255)
        max_value = np.max(tmp_bg)
        if max_value <= 1:
            return pt1, pt2


def approaching_vertical_point2(bg, line1):
    """

    """
    center_point = (line1[0][0] + line1[1][0]) / 2, (line1[0][1] + line1[1][1]) / 2 + 5
    pt1, pt2 = line1
    original_pt1, original_pt2 = copy.deepcopy(pt1), copy.deepcopy(pt2)
    original_pt1 = original_pt1[0], original_pt1[1] + 2
    original_pt2 = original_pt2[0], original_pt2[1] + 2
    pt1, pt2 = original_pt1, center_point
    while True:
        pt1, pt2 = translation_line_first_side(pt1, pt2, direction='up')
        tmp_bg = np.zeros_like(bg)
        tmp_bg = draw_line_from_points([pt1, pt2], tmp_bg, line_pixel=1)
        tmp_bg = tmp_bg + bg
        write_image('tmp_bg.jpg', tmp_bg * 255)
        max_value = np.max(tmp_bg)
        if max_value > 1:
            location = np.where(tmp_bg > 1)
            first_location, last_location = _sort_location(location)
            first_point = first_location
            break
    pt1, pt2 = center_point, original_pt2
    while True:
        pt1, pt2 = translation_line_second_side(pt1, pt2, direction='up')
        tmp_bg = np.zeros_like(bg)
        tmp_bg = draw_line_from_points([pt1, pt2], tmp_bg, line_pixel=1)
        tmp_bg = tmp_bg + bg
        write_image('tmp_bg.jpg', tmp_bg * 255)
        max_value = np.max(tmp_bg)
        if max_value > 1:
            location = np.where(tmp_bg > 1)
            first_location, last_location = _sort_location(location)
            second_point = first_location
            break
    pt1, pt2 = first_point, second_point
    while True:
        pt1, pt2 = translation_line(pt1, pt2, direction='down')
        tmp_bg = np.zeros_like(bg)
        tmp_bg = draw_line_from_points([pt1, pt2], tmp_bg, line_pixel=1)
        tmp_bg = tmp_bg + bg
        write_image('tmp_bg.jpg', tmp_bg * 255)
        max_value = np.max(tmp_bg)
        if max_value <= 1:
            return pt1, pt2
