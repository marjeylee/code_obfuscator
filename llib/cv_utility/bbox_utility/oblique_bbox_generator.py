# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     oblique_bbox_generator
   Description :
   Author :       'li'
   date：          2020/3/21
-------------------------------------------------
   Change Activity:
                   2020/3/21:
-------------------------------------------------
"""
import math

import cv2
import numpy as np

from llib.cv_utility.bbox_utility.bbox_utility import get_distance, resort_points
from llib.cv_utility.image_opt_utility import write_image, read_image


class ObliqueBBOXGenerator:
    """
    gen bbox and text area
    """

    def __init__(self, pixel):
        """
        0 <= pixel <= 1
        """
        self.enlarge_size = 0
        self.original_pixel = pixel
        self.format_pixel = self.__format_pixel()
        self.connected_labels_area, self.filter_labels = self.__get_connected_domains()
        self.pixel_contours = self.__get_all_contours()
        self.oblique_bbox = self.get_oblique_bbox()

    def __format_pixel(self):
        """
        format pixel
        """
        bg = np.zeros_like(self.original_pixel, dtype=np.uint8)
        bg[np.where(self.original_pixel > 0.6)] = 255
        return bg

    def __get_connected_domains(self):
        """
        combine and return connected domains
        :return:
        """
        _, labels = cv2.connectedComponents(self.format_pixel)
        shape = self.format_pixel.shape
        reshape_labels = labels.reshape(shape[0] * shape[1], )
        count = np.bincount(reshape_labels)[1:]
        filter_count = []
        for index, num in enumerate(count):
            connected_index = index + 1
            if num > 100:
                filter_count.append(connected_index)
        return labels, filter_count

    def __get_all_contours(self):
        """
        get all contours
        """
        all_contours = []
        for label_num in self.filter_labels:
            bg = np.zeros_like(self.connected_labels_area, dtype=np.uint8)
            bg[np.where(self.connected_labels_area == label_num)] = 255
            ret, thresh = cv2.threshold(bg, 127, 255, 0)
            try:
                contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            except:
                image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            if len(contours) == 0:
                continue
            if len(contours) == 1:
                all_contours.append(contours[0])
                continue
            max_size_contours = self._get_max_size_contours(contours)
            all_contours.append(max_size_contours)
        return all_contours

    def enlarge_bbox(self, bbox, img):
        """
        enlarge bbox
        :param enlarge_pixel:
        :param img:
        :param bbox:
        :return:
        """
        enlarge_pixel = self.enlarge_size
        p1, p2, p3, p4 = bbox[0], bbox[1], bbox[2], bbox[3]
        p1 = [p1[0] - enlarge_pixel, p1[1] - enlarge_pixel]
        p2 = [p2[0] + enlarge_pixel, p2[1] - enlarge_pixel]
        p3 = [p3[0] + enlarge_pixel, p3[1] + enlarge_pixel]
        p4 = [p4[0] - enlarge_pixel, p4[1] + enlarge_pixel]
        bbox = [p1, p2, p3, p4]
        img_height, img_width, _ = img.shape
        for point in bbox:
            width, height = point
            if width < 0:
                point[0] = 0
            if height < 0:
                point[1] = 0
            if height > img_height:
                point[1] = img_height
            if width > img_width:
                point[0] = img_width
        return bbox

    def get_oblique_bbox(self):
        """
        gen bbox
        """
        oblique_bbox = []
        for contours in self.pixel_contours:
            bbox, is_rect = self.__get_bbox_by_contours(contours)
            bbox = np.array(bbox) * 2
            bbox = bbox.astype(np.int)
            bbox = bbox.tolist()
            oblique_bbox.append(bbox)
        return oblique_bbox

    @staticmethod
    def _get_max_size_contours(contours):
        """
        get max siz contours
        """
        return_contours = contours[0]
        length = len(contours)
        for i in range(1, length):
            ret_size = return_contours.shape[0]
            new_size = contours[i].shape[0]
            if ret_size < new_size:
                return_contours = contours[i]
        return return_contours

    @staticmethod
    def __get_bbox_by_contours(contour):
        """
        get bbox by contours
        """
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        return resort_points(box), False

        for epsilon in [0, 1, 3, 8, 10]:
            approx = cv2.approxPolyDP(contour, epsilon, True)
            approx_shape = approx.shape
            if approx_shape[0] < 4:
                rect = cv2.minAreaRect(contour)
                box = cv2.boxPoints(rect)
                return resort_points(box), False
            if approx_shape[0] == 4:
                box = np.squeeze(approx, axis=1)
                box = resort_points(box)
                return box, True
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        return resort_points(box), True

    @staticmethod
    def get_point_line_distance(point, line):
        point_x = point[0]
        point_y = point[1]
        line_s_x = line[0][0]
        line_s_y = line[0][1]
        line_e_x = line[1][0]
        line_e_y = line[1][1]
        # 若直线与y轴平行，则距离为点的x坐标与直线上任意一点的x坐标差值的绝对值
        if line_e_x - line_s_x == 0:
            return math.fabs(point_x - line_s_x)
        # 若直线与x轴平行，则距离为点的y坐标与直线上任意一点的y坐标差值的绝对值
        if line_e_y - line_s_y == 0:
            return math.fabs(point_y - line_s_y)
        # 斜率
        k = (line_e_y - line_s_y) / (line_e_x - line_s_x)
        # 截距
        b = line_s_y - k * line_s_x
        # 带入公式得到距离dis
        dis = math.fabs(k * point_x - point_y + b) / math.pow(k * k + 1, 0.5)
        return dis

    @staticmethod
    def __get_area_shape(bbox):
        """
        get area shape
        :param bbox:
        :return:
        """
        # height = ObliqueBBOXGenerator.get_point_line_distance(bbox[1], [bbox[0], bbox[3]])
        # width = ObliqueBBOXGenerator.get_point_line_distance(bbox[1], [bbox[0], bbox[3]])
        len_1, len_2, len_3, len_4 = get_distance(bbox[0], bbox[1]), get_distance(bbox[1], bbox[2]), \
                                     get_distance(bbox[2], bbox[3]), get_distance(bbox[3], bbox[0])
        tmp_width_max = int(max(len_1, len_3))
        tmp_height_max = int(max(len_4, len_2))
        is_horizontal = tmp_width_max > tmp_height_max
        if is_horizontal:
            return tmp_width_max, tmp_height_max
        return tmp_height_max, tmp_width_max
        # is_horizontal = len_1 > len_2
        # if is_horizontal:
        #     width = len_1
        # else:
        #     height = len_2
        # return int(height), int(width)

    @staticmethod
    def get_transparent_text_area(original_image, original_bboxs):
        """
        get transparent text area
        :param original_image:
        :param original_bboxs:
        :return:
        """
        areas = []
        for bbox in original_bboxs:
            area_width, area_height = ObliqueBBOXGenerator.__get_area_shape(bbox)
            pts1 = np.float32([bbox[0], bbox[1], bbox[3], bbox[2]])
            pts2 = np.float32([[0, 0], [0, area_width], [area_height, 0], [area_height, area_width]])
            transform = cv2.getPerspectiveTransform(pts1, pts2)
            dst = cv2.warpPerspective(original_image, transform, (area_height, area_width))
            dst = np.flip(dst, axis=0)
            dst = np.rot90(dst)
            dst = np.rot90(dst)
            dst = np.rot90(dst)
            areas.append(dst)
        return areas


def main():
    original_pixel = cv2.imread('pxl.jpg')[:, :, 0] / 255
    bbox_gen = ObliqueBBOXGenerator(original_pixel)
    oblique_bbox = bbox_gen.get_oblique_bbox()
    img = read_image('imgs/1.jpg')
    areas = bbox_gen.get_transparent_text_area(img, oblique_bbox)
    for area in areas:
        write_image('ar.jpg', area)


if __name__ == '__main__':
    main()
