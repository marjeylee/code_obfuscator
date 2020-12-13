# -*- coding: utf-8 -*-
"""
-------------------------------------------------
File Name： container_bbox_generate
Description :
Author : 'li'
date： 2020/10/28
-------------------------------------------------
Change Activity:
2020/10/28:
-------------------------------------------------
"""
import time

import cv2
import numpy as np

from llib.cv_utility.bbox_utility.bbox_utility import resort_points
from llib.cv_utility.bbox_utility.draw_line_from_point import draw_line_from_points
from llib.cv_utility.image_opt_utility import read_image, write_image, enlarge_bbox


class ContainerBboxGenerate:
    def __init__(self, text_area_pixel, gap_area_pixel, threshold=0.8, min_bbox_pixel_size=20,
                 good_points_distance=3, is_corrected=True):
        """
        container bbox generate
        :param text_area_pixel:
        :param gap_area_pixel:
        """
        self.good_points_distance = good_points_distance
        self.is_corrected = is_corrected
        self.original_textarea_pixel = text_area_pixel
        self.original_gap_area_pixel = gap_area_pixel
        self.threshold = threshold
        self.min_bbox_pixel_size = min_bbox_pixel_size
        self.format_textarea_pixel, self.format_gap_area_pixel = self._format_original_pixel()

    def _format_original_pixel(self):
        """
        format pixel by threshold
        :return:
        """
        area = np.zeros_like(self.original_textarea_pixel, dtype=np.int)
        area[np.where(self.original_textarea_pixel > self.threshold)] = 255
        gap = np.zeros_like(self.original_gap_area_pixel, dtype=np.int)
        gap[np.where(self.original_gap_area_pixel > self.threshold - 0.2)] = 255
        return area, gap

    def gen_bbox(self):
        """

        :return:
        """
        line_points = self._get_gap_lines()
        bg = np.zeros_like(self.original_textarea_pixel, dtype=np.int)
        for point in line_points:
            tmp_canvas = draw_line_from_points(point, bg)
            bg = bg + tmp_canvas
        # write_image('line.jpg', bg * 255)
        bg = self.format_textarea_pixel - bg

        bg[np.where(bg < 0)] = 0
        # write_image('pix.jpg', bg * 255)
        text_area_domain = ContainerBboxGenerate._get_connected_domain(bg)
        bboxes = self._gen_bboxes_by_domain(text_area_domain)
        return bboxes

    @staticmethod
    def _get_single_by_domain(domain):
        """
        domain
        :param domain:
        :return:
        """
        ret, thresh = cv2.threshold(domain, 127, 255, 0)
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) == 0:
            return None
        rect = cv2.minAreaRect(contours[0])
        box = cv2.boxPoints(rect)
        box = resort_points(box)
        return box

    # def _get_single_by_domain(self, bg, locations):
    #     """
    #     domain
    #     :return:
    #     """
    #     h, w = bg.shape[0], bg.shape[1]
    #     tmp_bg = np.zeros((1, w))
    #     bg = np.concatenate((tmp_bg, bg, tmp_bg), axis=0)
    #     tmp_bg = np.zeros((h + 2, 1))
    #     bg = np.concatenate((tmp_bg, bg, tmp_bg), axis=1)
    #     bg = bg.astype(np.uint8)
    #     corners = cv2.goodFeaturesToTrack(bg, 12, 0.03, self.good_points_distance)
    #     corners = np.int0(corners)
    #     corners = corners[:, 0, :]
    #     if corners.shape[0] < 4 or self.is_corrected is False:
    #         ret, thresh = cv2.threshold(bg, 127, 255, 0)
    #         contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #         if len(contours) == 0:
    #             return None
    #         if len(contours) > 1:
    #             contours = self._get_max_size_contours(contours)
    #         rect = cv2.minAreaRect(contours[0])
    #         box = cv2.boxPoints(rect)
    #         return box
    #     if corners.shape[0] == 4:
    #         return corners
    #     if corners.shape[0] > 4:
    #         return self.format_corners(corners, locations)
    #     return corners

    @staticmethod
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

    @staticmethod
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

    def format_corners(self, corners, locations):
        """
        format corners
        """
        center_point = np.array([locations[1].mean(), locations[0].mean()])
        base_vector = np.array([10, 0])
        points_size = corners.shape[0]
        new_corners_up_side = []
        new_corners_down_side = []
        for i in range(points_size):
            current_point = corners[i, :]
            tmp_vector = current_point - center_point
            angle = self.get_angle_by_vector(base_vector, tmp_vector)
            if current_point[1] < center_point[1]:
                new_corners_up_side.append([angle, current_point])
            else:
                new_corners_down_side.append([angle, current_point])
        new_corners_up_side = self._sort_lst(new_corners_up_side)
        new_corners_down_side = list(reversed(self._sort_lst(new_corners_down_side)))
        sorted_lst = new_corners_up_side + new_corners_down_side
        return self._get_format_points(sorted_lst)

    def get_corners_mapping(self, corners):
        """
        get corners mapping
        """
        corners_size = len(corners)
        corners_angle_mapping = {}
        for i in range(1, corners_size - 1):
            last_point = corners[i - 1]
            current_point = corners[i]
            next_point = corners[i + 1]
            angle = self._get_angle(last_point, current_point, next_point)
            corners_angle_mapping[i] = angle
        """first point"""
        last_point = corners[- 1]
        current_point = corners[0]
        next_point = corners[1]
        angle = self._get_angle(last_point, current_point, next_point)
        corners_angle_mapping[0] = angle
        """ last point"""
        last_point = corners[- 2]
        current_point = corners[-1]
        next_point = corners[0]
        angle = self._get_angle(last_point, current_point, next_point)
        corners_angle_mapping[corners_size - 1] = angle
        return corners_angle_mapping

    def _get_format_points(self, sorted_lst):
        """
        get format points
        """
        corners = []
        for item in sorted_lst:
            corners.append(item[1])
        corners = np.array(corners)
        res = self.get_corners_mapping(corners)
        sort_res = sorted(res.items(), key=lambda x: x[1])
        format_points = []
        for i in range(4):
            index = sort_res[i][0]
            format_points.append(corners[index, :])
        return np.array(format_points)

    @staticmethod
    def get_angle_by_vector(v1, v2):
        """
        get angle by vector
        """
        a_norm = np.linalg.norm(v1)
        b_norm = np.linalg.norm(v2)
        a_dot_b = v1.dot(v2)
        cos_theta = np.arccos(a_dot_b / (a_norm * b_norm))
        return np.rad2deg(cos_theta)

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

    def _gen_bboxes_by_domain(self, domain):
        """
        gen bboxes by domain
        :param domain:
        :return:
        """
        domain_max_value = domain.max()
        bboxes = []
        for i in range(1, domain_max_value + 1):
            locations = np.where(domain == i)
            if locations[0].size < self.min_bbox_pixel_size:
                continue
            bg = np.zeros_like(domain, dtype=np.uint8)
            bg[locations] = 255
            bbox = self._get_single_by_domain(bg)
            if bbox is not None and bbox.shape[0] == 4:
                bbox = resort_points(bbox)
                bbox = np.array(enlarge_bbox(1, bbox, domain.shape))
                bboxes.append(bbox * 2)
        return bboxes

    def _get_gap_lines(self):
        """
        gen gap line from gap area
        :return:
        """
        intersection_area = self._get_intersection_area()
        intersection_domain = ContainerBboxGenerate._get_connected_domain(intersection_area)
        gap_domain = ContainerBboxGenerate._get_connected_domain(self.format_gap_area_pixel)
        domain_max_value = intersection_domain.max()
        if domain_max_value == 0:
            return []
        gap_lines = []
        for i in range(1, domain_max_value + 1):  # for each domain
            xs, ws = np.where(intersection_domain == i)
            x, y = xs[0], ws[0]
            domain_value = gap_domain[x, y]
            selected_domain_area = np.zeros_like(gap_domain, dtype=np.uint8)
            selected_domain_area[np.where(gap_domain == domain_value)] = 255
            points = ContainerBboxGenerate._gen_bbox_by_domain(selected_domain_area)
            # points = (np.array([points[0][0], points[0][1] + 1]), np.array([points[1][0], points[1][1] + 1]))
            gap_lines.append(points)
        return gap_lines

    def _get_intersection_area(self):
        """
        get intersection area
        :return:
        """
        tmp_area = self.format_textarea_pixel + self.format_gap_area_pixel
        intersection_area = np.zeros_like(tmp_area, np.uint8)
        intersection_area[np.where(tmp_area > 300)] = 255
        return intersection_area

    @staticmethod
    def _get_connected_domain(intersection_area):
        """
        get connected domain
        :param intersection_area:
        :return:
        """
        tmp_area = intersection_area.astype(np.uint8)
        _, labels_image = cv2.connectedComponents(tmp_area, connectivity=4)
        return labels_image

    @staticmethod
    def _gen_bbox_by_domain(selected_domain_area):
        ret, thresh = cv2.threshold(selected_domain_area, 127, 255, 0)
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        rect = cv2.minAreaRect(contours[0])
        box = cv2.boxPoints(rect)
        box = resort_points(box)
        point_1, point_2 = (box[0] + box[3]) / 2, (box[1] + box[2]) / 2
        return point_1.astype(np.int), point_2.astype(np.int)


def main():
    for i in range(10):
        start_time = time.time()
        text_area = read_image('imgs/txt.jpg')
        gap_area = read_image('imgs/gap.jpg')
        bbox_generator = ContainerBboxGenerate(text_area / 255, gap_area / 255)
        bbox_generator.gen_bbox()
        print(time.time() - start_time)


if __name__ == '__main__':
    main()
