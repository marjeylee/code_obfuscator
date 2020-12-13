import numpy as np

from llib.cv_utility.bbox_utility.bbox_utility import get_distance


class BBoxCorrection:
    def __init__(self, area_pixel, bbox):
        """

        :param area_pixel:
        :param bbox:
        """
        self.area_pixel = area_pixel
        self.bbox = bbox
        self.left_point_size = self._get_left_move_points()
        self.right_point_size = self._get_right_move_points()
        self.first_line_ratio = self._get_line_ratio(bbox[0], bbox[1])
        self.second_line_ratio = self._get_line_ratio(bbox[3], bbox[2])

    @staticmethod
    def _get_line_ratio(point0, point1):
        distance = get_distance(point0, point1)
        h_ratio = (point1[0] - point0[0]) / distance
        w_ratio = (point1[1] - point0[1]) / distance
        return h_ratio, w_ratio

    def corrected(self):
        w, h = self.bbox[0]
        step = self.left_point_size[0]
        new_w, new_h = int(w + step * self.first_line_ratio[0]), int(h + step * self.first_line_ratio[1])
        point0 = [new_w, new_h]
        w, h = self.bbox[1]
        step = self.right_point_size[0]
        new_w, new_h = int(w + step * self.first_line_ratio[0]), int(h + step * self.first_line_ratio[1])
        point1 = [new_w, new_h]
        """==="""
        w, h = self.bbox[2]
        step = self.right_point_size[1]
        new_w, new_h = int(w + step * self.second_line_ratio[0]), int(h + step * self.second_line_ratio[1])
        point2 = [new_w, new_h]
        w, h = self.bbox[3]
        step = self.left_point_size[1]
        new_w, new_h = int(w + step * self.second_line_ratio[0]), int(h + step * self.second_line_ratio[1])
        point3 = [new_w, new_h]
        # points = self._format_points([point0, point1, point2, point3])
        return [point0, point1, point2, point3]

    def _get_right_move_points(self):
        h, w = self.area_pixel.shape
        left_area = self.area_pixel[:, w // 2:]
        one_forth_point = h // 4
        third_forth_point = h * 3 // 4
        one_forth_area = left_area[one_forth_point, :][::-1]
        third_forth_area = left_area[third_forth_point, :][::-1]
        one_forth_size = 0
        for i in range(one_forth_area.size):
            if one_forth_area[i] != 0:
                one_forth_size = i
                break
        third_forth_size = 0
        for i in range(third_forth_area.size):
            if third_forth_area[i] != 0:
                third_forth_size = i
                break
        if one_forth_size == third_forth_size:
            return [0, -0]
        if one_forth_size > third_forth_size:
            return [- one_forth_size, one_forth_size]
        return [third_forth_size, -third_forth_size]

    def _get_left_move_points(self):
        h, w = self.area_pixel.shape
        left_area = self.area_pixel[:, :w // 2]
        one_forth_point = h // 4
        third_forth_point = h * 3 // 4
        one_forth_area = left_area[one_forth_point, :]
        third_forth_area = left_area[third_forth_point, :]
        one_forth_size = 0  # np.where(one_forth_area == 0)[0].size
        for i in range(one_forth_area.size):
            if one_forth_area[i] != 0:
                one_forth_size = i
                break
        third_forth_size = 0
        for i in range(third_forth_area.size):
            if third_forth_area[i] != 0:
                third_forth_size = i
                break
        if one_forth_size == third_forth_size:
            return [0, -0]
        if one_forth_size > third_forth_size:
            return [one_forth_size, -one_forth_size]
        return [-third_forth_size, third_forth_size]
