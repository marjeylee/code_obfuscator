# -*- coding: utf-8 -*-
"""
-------------------------------------------------
File Name： bbox_resort
Description :
Author : 'li'
date： 2020/9/24
-------------------------------------------------
Change Activity:
2020/9/24:
-------------------------------------------------
"""
import numpy as np


def _get_center_point(points):
    ws = points[:, 0]
    hs = points[:, 1]
    center_point = np.array([ws.mean(), hs.mean()])
    return center_point


def _get_angle(last_point, current_point, next_point):
    """
    get angle by vector
    """
    v1 = last_point - current_point
    v2 = next_point - current_point
    a_norm = np.linalg.norm(v1)
    b_norm = np.linalg.norm(v2)
    a_dot_b = v1.dot(v2)
    if (a_dot_b / (a_norm * b_norm)) <= -1:
        return 180
    cos_theta = np.arccos(a_dot_b / (a_norm * b_norm))
    return np.rad2deg(cos_theta)


def _get_angle_by_vector(v1, v2):
    """
    get angle by vector
    """
    a_norm = np.linalg.norm(v1)
    b_norm = np.linalg.norm(v2)
    a_dot_b = v1.dot(v2)
    cos_theta = np.arccos(a_dot_b / (a_norm * b_norm))
    return np.rad2deg(cos_theta)


def _sort_lst(current_lst):
    total_size = len(current_lst)
    if total_size > 1:
        for i in range(total_size - 1):
            for j in range(i + 1, total_size):
                tmp_vector = current_lst[i]
                if current_lst[i][0] > current_lst[j][0]:
                    current_lst[i] = current_lst[j]
                    current_lst[j] = tmp_vector
    return current_lst


def _get_corners_mapping(corners):
    """
    get corners mapping
    """
    corners_size = len(corners)
    corners_angle_mapping = {}
    for i in range(1, corners_size - 1):
        last_point = corners[i - 1]
        current_point = corners[i]
        next_point = corners[i + 1]
        angle = _get_angle(last_point, current_point, next_point)
        corners_angle_mapping[i] = angle
    """first point"""
    last_point = corners[- 1]
    current_point = corners[0]
    next_point = corners[1]
    angle = _get_angle(last_point, current_point, next_point)
    corners_angle_mapping[0] = angle
    """ last point"""
    last_point = corners[- 2]
    current_point = corners[-1]
    next_point = corners[0]
    angle = _get_angle(last_point, current_point, next_point)
    corners_angle_mapping[corners_size - 1] = angle
    return corners_angle_mapping


def _get_format_points(sorted_lst):
    """
    get format points
    """
    corners = []
    for item in sorted_lst:
        corners.append(item[1])
    corners.reverse()
    corners = np.array(corners)
    return corners


def _determine_is_horizontal_box(box):
    height = max(abs(box[0][1] - box[1][1]), abs(box[0][1] - box[2][1]))
    width = max(abs(box[0][0] - box[1][0]), abs(box[0][0] - box[2][0]))
    if width > height:
        return True
    return False


def _get_left_top_point_index(new_bbox, center_point):
    """
    new bbox center point
    """
    if _determine_is_horizontal_box(new_bbox):
        tmp_point_index = None
        for i in range(4):
            current_point = new_bbox[i, :]
            if current_point[0] < center_point[0]:
                if tmp_point_index is None:

                    tmp_point_index = i
                elif new_bbox[tmp_point_index, :][1] > current_point[1]:
                    tmp_point_index = i
        if tmp_point_index is not None:
            return tmp_point_index
        return 2
    else:
        tmp_point_index = None
        for i in range(4):
            current_point = new_bbox[i, :]
            if current_point[1] < center_point[1]:
                if tmp_point_index is None:
                    tmp_point_index = i
                elif new_bbox[tmp_point_index, :][0] > current_point[0]:
                    tmp_point_index = i
        if tmp_point_index is not None:
            return tmp_point_index
        return 2


def _format_new_bbox(new_bbox, center_point):
    box_array = new_bbox.tolist()
    box_array = box_array + box_array
    if new_bbox.shape[0] == 4:
        index = _get_left_top_point_index(new_bbox, center_point)
        new_format_box = np.array(box_array[index:index + 4])
        return new_format_box
    return new_bbox


def resort_points_v2(points):
    """
    resort points v2
    points format (width,height)
    """
    points = np.array(points)
    center_point = _get_center_point(points)
    points_size = points.shape[0]
    new_corners_up_side = []
    new_corners_down_side = []
    base_vector = np.array([10, 0])
    for i in range(points_size):
        current_point = points[i, :]
        tmp_vector = current_point - center_point
        angle = _get_angle_by_vector(base_vector, tmp_vector)
        if current_point[1] < center_point[1]:
            new_corners_up_side.append([angle, current_point])
        else:
            new_corners_down_side.append([angle, current_point])
    new_corners_up_side = _sort_lst(new_corners_up_side)
    new_corners_down_side = list(reversed(_sort_lst(new_corners_down_side)))
    sorted_lst = new_corners_up_side + new_corners_down_side
    new_bbox = _get_format_points(sorted_lst)
    new_bbox = _format_new_bbox(new_bbox, center_point)
    return new_bbox


def main():
    points = [[292, 269], [291, 281], [320, 297], [322, 316]]
    points = resort_points_v2(points)
    print(points)


if __name__ == '__main__':
    main()
