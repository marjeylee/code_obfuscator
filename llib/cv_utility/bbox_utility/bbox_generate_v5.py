import cv2

from llib.cv_utility.bbox_utility.bbox_utility import resort_points
from llib.cv_utility.bbox_utility.draw_bbox import draw_bbox
from llib.cv_utility.bbox_utility.get_text_area_from_points import get_text_area_from_bbox
from llib.cv_utility.image_opt_utility import read_image, write_image
import numpy as np


class BboxGeneratorV5:
    def __init__(self, pixel, threshold=0.6,
                 min_pixel_size=10,
                 is_corrected=True,
                 enlarge_bbox_ratio=2,
                 enlarge_bbox_pixel=1,
                 good_points_distance=6):
        """

        :param pixel:
        :param threshold:
        :param min_pixel_size:
        """
        self.enlarge_bbox_pixel = enlarge_bbox_pixel
        self.enlarge_bbox_ratio = enlarge_bbox_ratio
        self.min_pixel_size = min_pixel_size
        self.pixel_threshold = threshold
        self.is_corrected = is_corrected
        self.text_area_pixel = pixel
        self.format_pixel = self._format_pixel()
        self.connected_domain = self.__get_connected_domains()
        self.good_points_distance = good_points_distance

    @staticmethod
    def enlarge_bbox(enlarge_pixel, bbox, shape):
        """
        enlarge bbox
        :param enlarge_pixel:
        :param shape:
        :param bbox:
        :return:
        """

        p1, p2, p3, p4 = bbox[0], bbox[1], bbox[2], bbox[3]
        bbox = np.array(bbox)
        center_point = bbox[:, 0].mean(), bbox[:, 1].mean()
        bbox = []
        for p in [p1, p2, p3, p4]:
            p = BboxGeneratorV5._enlarge_point(p, center_point, enlarge_pixel)
            bbox.append(p)
        img_height, img_width = shape[0], shape[1]
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

    def gen_bboxes(self):
        """
        interface
        :return:
        """
        domain_max_value = self.connected_domain.max()
        if domain_max_value == 0:
            return []
        bboxes = []
        for i in range(1, domain_max_value + 1):  # for each domain
            box = self._get_single_bbox(i)
            if box is not None:
                box = np.array(box) - 1
                box = resort_points(box)
                box = self.enlarge_bbox(self.enlarge_bbox_pixel, box, self.format_pixel.shape)
                box = np.array(box) * self.enlarge_bbox_ratio
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
        h, w = bg.shape[0], bg.shape[1]
        tmp_bg = np.zeros((1, w))
        bg = np.concatenate((tmp_bg, bg, tmp_bg), axis=0)
        tmp_bg = np.zeros((h + 2, 1))
        bg = np.concatenate((tmp_bg, bg, tmp_bg), axis=1)
        bg = bg.astype(np.uint8)
        corners = cv2.goodFeaturesToTrack(bg, 12, 0.03, self.good_points_distance)
        corners = np.int0(corners)
        corners = corners[:, 0, :]
        # print(corners.tolist())
        if corners.shape[0] < 4 or self.is_corrected is False:
            ret, thresh = cv2.threshold(bg, 127, 255, 0)
            contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            if len(contours) == 0:
                return None
            if len(contours) > 1:
                contours = self._get_max_size_contours(contours)
            rect = cv2.minAreaRect(contours[0])
            box = cv2.boxPoints(rect)
            return box
        if corners.shape[0] == 4:
            return corners
        if corners.shape[0] > 4:
            return self.format_corners(corners, locations)
        return corners

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

    def format_corners(self, corners, locations):
        """
        format corners
        """
        center_point = np.array([locations[1].mean(), locations[0].mean()])
        base_vector = np.array([10, 0])
        points_size = corners.shape[0]
        new_corners_up_side = []
        new_corners_down_side = []
        # img = read_image('final.jpg')
        # res = draw_bbox(corners, img)
        # write_image('ll.jpg', res)
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
    def _enlarge_point(p, center_point, enlarge_pixel):
        """
        enlarge point
        """
        res = p - center_point
        w, h = res[0], res[1]
        if w > 0:
            p[0] = p[0] + enlarge_pixel
        if w < 0:
            p[0] = p[0] - enlarge_pixel
        if h > 0:
            p[1] = p[1] + enlarge_pixel
        if h < 0:
            p[1] = p[1] - enlarge_pixel
        return p


def main():
    pixel = read_image('imgs/pixl.jpg') / 255
    bbox = BboxGeneratorV5(pixel, is_corrected=True).gen_bboxes()
    print(bbox)


if __name__ == '__main__':
    main()
