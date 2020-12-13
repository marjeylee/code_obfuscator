import copy

import cv2

from llib.cv_utility.bbox_utility.bbox_correction import BBoxCorrection
from llib.cv_utility.bbox_utility.bbox_utility import resort_points
from llib.cv_utility.bbox_utility.draw_line_from_point import translation_line, draw_line_from_points, \
    translation_line_first_side, translation_line_second_side
from llib.cv_utility.bbox_utility.get_text_area_from_points import get_text_area_from_bbox
from llib.cv_utility.image_opt_utility import read_image, write_image
import numpy as np


class BboxGeneratorV2:
    def __init__(self, pixel, threshold=0.6, min_pixel_size=10, is_corrected=True):
        """

        :param pixel:
        :param threshold:
        :param min_pixel_size:
        """
        self.min_pixel_size = min_pixel_size
        self.pixel_threshold = threshold
        self.is_corrected = is_corrected
        self.text_area_pixel = pixel
        self.format_pixel = self._format_pixel()
        self.connected_domain = self.__get_connected_domains()

    def gen_bboxes(self):
        """
        interface
        :return:
        """
        domain_max_value = self.connected_domain.max()
        if domain_max_value == 0:
            return []
        bboxes = []
        for i in range(1, domain_max_value + 1):
            box = self._get_single_bbox(i)
            self._format_points(box)
            if box is not None:
                bboxes.append(box)
        return bboxes

    def __get_connected_domains(self):
        """
        combine and return connected domains
        :return:
        """
        _, labels_image = cv2.connectedComponents(self.format_pixel)
        return labels_image

    def _format_pixel(self):
        bg = np.zeros_like(self.text_area_pixel, dtype=np.uint8)
        bg[np.where(self.text_area_pixel > self.pixel_threshold)] = 255
        return bg

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

    def _get_single_bbox(self, i):
        """
        get single bbox
        :param i:
        :return:
        """
        locations = np.where(self.connected_domain == i)
        if locations[0].size < self.min_pixel_size:
            return None
        bg = np.zeros_like(self.connected_domain, dtype=np.uint8)
        bg[locations] = 255
        ret, thresh = cv2.threshold(bg, 127, 255, 0)
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) == 0:
            return None
        if len(contours) > 1:
            contours = self._get_max_size_contours(contours)
        bbox = self._get_box_by_contours(contours[0])
        bg = np.zeros_like(self.connected_domain, dtype=np.uint8)
        bg[locations] = 1
        self.__corrected_bbox_second_time(bg, bbox)
        return bbox

    def _get_box_by_contours(self, contour):
        """
        get box by contours
        :return:
        """
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        box = resort_points(box)
        if not self.is_corrected:
            return box
        area_pixel = get_text_area_from_bbox(self.format_pixel, box)
        if area_pixel is None:
            return None
        box = self._corrected_bbox(box, area_pixel)
        box = resort_points(box)

        return box

    @staticmethod
    def _corrected_bbox(box, area_pixel):
        """

        :param box:
        :param area_pixel:
        :return:
        """
        h, w = area_pixel.shape
        if h > w:
            return box
        return BBoxCorrection(area_pixel, box).corrected()

    def _format_points(self, box):
        """
        format points
        """
        if box is None:
            return None
        box = np.array(box)
        box[np.where(box < 0)] = 0
        return box

    def __corrected_bbox_second_time(self, bg, bbox):
        """
        corrected second time
        """
        center_point = (bbox[0][0] + bbox[2][0]) / 2, (bbox[0][1] + bbox[2][1]) / 2
        des_line = np.zeros_like(bg)
        bbox[0], bbox[1] = self.get_new_corrected_point(bg, bbox[0], bbox[1], direction='down')
        bbox[1], bbox[2] = self.get_new_corrected_point(bg, bbox[1], bbox[2], direction='left')
        bbox[2], bbox[3] = self.get_new_corrected_point(bg, bbox[2], bbox[3], direction='up')
        bbox[3], bbox[1] = self.get_new_corrected_point(bg, bbox[3], bbox[0], direction='right')
        des_line = draw_line_from_points([bbox[0], bbox[1]], des_line, line_pixel=1)
        des_line = draw_line_from_points([bbox[1], bbox[2]], des_line, line_pixel=1)
        des_line = draw_line_from_points([bbox[2], bbox[3]], des_line, line_pixel=1)
        des_line = draw_line_from_points([bbox[3], bbox[0]], des_line, line_pixel=1)
        write_image('des_line.jpg', des_line * 255)

    @staticmethod
    def get_new_corrected_point(bg, pt1, pt2, direction='down'):
        """
        get new corrected points
        """
        original_pt1, original_pt2 = copy.deepcopy(pt1), copy.deepcopy(pt2)
        is_move_points = False

        while True:
            last_pt1, last_pt2 = copy.deepcopy(pt1), copy.deepcopy(pt2)
            pt1, pt2 = translation_line(pt1, pt2, direction=direction)
            tmp_bg = np.zeros_like(bg)
            tmp_bg = draw_line_from_points([pt1, pt2], tmp_bg, line_pixel=1)
            tmp_bg = tmp_bg + bg
            max_value = np.max(tmp_bg)
            if max_value <= 1:
                is_move_points = True
            else:
                break
        write_image('tmp_bg.jpg', tmp_bg * 255)
        if is_move_points:
            pt1, pt2 = last_pt1, last_pt2
            original_pt1, original_pt2 = copy.deepcopy(pt1), copy.deepcopy(pt2)
        """first side"""
        while True:
            last_pt1, last_pt2 = copy.deepcopy(original_pt1), copy.deepcopy(original_pt2)
            pt1, pt2 = translation_line_first_side(pt1, pt2, direction=direction)
            tmp_bg = np.zeros_like(bg)
            tmp_bg = draw_line_from_points([pt1, pt2], tmp_bg, line_pixel=1)
            tmp_bg = tmp_bg + bg
            max_value = np.max(tmp_bg)
            if max_value <= 1:
                is_move_points = True
            else:
                break
        write_image('tmp_bg.jpg', tmp_bg * 255)
        final_pt1, final_pt2 = None, None
        if is_move_points:
            final_pt1 = last_pt1
        """second side"""
        while True:
            last_pt1, last_pt2 = copy.deepcopy(original_pt1), copy.deepcopy(original_pt2)
            pt1, pt2 = translation_line_second_side(pt1, pt2, direction=direction)
            tmp_bg = np.zeros_like(bg)
            tmp_bg = draw_line_from_points([pt1, pt2], tmp_bg, line_pixel=1)
            tmp_bg = tmp_bg + bg
            max_value = np.max(tmp_bg)
            if max_value <= 1:
                is_move_points = True
            else:
                break
        if is_move_points:
            final_pt2 = last_pt2
        write_image('tmp_bg.jpg', tmp_bg * 255)
        if is_move_points:
            tmp_bg = draw_line_from_points([final_pt1, final_pt2], tmp_bg, line_pixel=1)
            tmp_bg = tmp_bg + bg
            write_image('tmp_bg.jpg', tmp_bg * 255)
            return final_pt1, final_pt2
        return original_pt1, original_pt2


def main():
    pixel = read_image('txt.jpg') / 255
    bbox = BboxGeneratorV2(pixel, is_corrected=True).gen_bboxes()
    for box in bbox:
        img = read_image('txt.jpg')
        area = get_text_area_from_bbox(img, box)
        write_image('area.jpg', area)


if __name__ == '__main__':
    main()
