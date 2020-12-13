import numpy as np
import cv2

from llib.cv_utility.bbox_utility.bbox_resort_v2 import resort_points_v2
from llib.cv_utility.bbox_utility.bbox_utility import get_distance


def __get_area_shape(bbox):
    """
    get area shape
    :param bbox:
    :return:
    """
    len_1, len_2 = get_distance(bbox[0], bbox[1]), get_distance(bbox[1], bbox[2])
    return int(len_1), int(len_2)


def transform_image(bbox, dst):
    """
    pass
    """
    center_point_1 = bbox[0][0] + bbox[1][0], bbox[0][1] + bbox[1][1]
    center_point_2 = bbox[2][0] + bbox[3][0], bbox[2][1] + bbox[3][1]
    if center_point_1[0] < center_point_2[0]:
        left_height = center_point_1[1]
        right_height = center_point_2[1]
    else:
        left_height = center_point_2[1]
        right_height = center_point_1[1]
    if right_height < left_height:
        dst = np.rot90(dst)
        dst = np.rot90(dst)

        dst = np.rot90(dst)
    else:
        dst = np.rot90(dst)
    return dst


def get_text_area_from_bbox(original_image, bbox):
    """
    get text area
    """
    bbox = resort_points_v2(bbox)
    area_width, area_height = __get_area_shape(bbox)
    pts1 = np.float32([bbox[0], bbox[1], bbox[3], bbox[2]])
    pts2 = np.float32([[0, 0], [0, area_width], [area_height, 0], [area_height, area_width]])
    transform = cv2.getPerspectiveTransform(pts1, pts2)
    dst = cv2.warpPerspective(original_image, transform, (area_height, area_width))
    dst = np.rot90(dst)
    dst = np.flip(dst, axis=0)
    if area_height > area_width:
        dst = transform_image(bbox, dst)
    if area_width < 6 or area_height < 6:
        return None
    return dst
