import cv2
import numpy as np


def _get_k_b(points):
    """
    get line`s  k b
    """
    p1, p2 = points[0], points[1]
    x1, y1 = p1
    x2, y2 = p2
    k = (y1 - y2) / ((x1 - x2) + 10e-9)
    b = (x1 * y2 - x2 * y1) / ((x1 - x2) + 10e-9)
    return k, b


def _get_new_points(points):
    k, b = _get_k_b(points)
    x0, x1 = 0, 2000
    y0 = b
    y1 = 2000 * k + b
    return (x0, int(y0)), (x1, int(y1))


def draw_line_from_points(points, img, line_pixel=255):
    """
    """
    shape = img.shape
    canvas = np.zeros(shape, dtype="uint8")  # 3
    if len(points) == 0:
        return canvas

    # if points[0][0] == points[1][0]:
    #     new_p1, new_p2 = (int(points[0][0]), 0), (int(points[0][0]), 2000)
    # else:
    #     new_p1, new_p2 = _get_new_points(points)
    # cv2.line(canvas, new_p1, new_p2, line_pixel)  # 5
    cv2.line(canvas, (int(points[0][0]), int(points[0][1])), (int(points[1][0]), int(points[1][1])), line_pixel,
             thickness=2)  # 5
    return canvas


def translation_line(pt1, pt2, direction='left', move_step=1):
    """

    """
    if direction == 'left':
        pt1 = pt1[0] - move_step, pt1[1]
        pt2 = pt2[0] - move_step, pt2[1]
        return pt1, pt2
    if direction == 'right':
        pt1 = pt1[0] + move_step, pt1[1]
        pt2 = pt2[0] + move_step, pt2[1]
        return pt1, pt2
    if direction == 'down':
        pt1 = pt1[0], pt1[1] + move_step
        pt2 = pt2[0], pt2[1] + move_step
        return pt1, pt2
    if direction == 'up':
        pt1 = pt1[0], pt1[1] - move_step
        pt2 = pt2[0], pt2[1] - move_step
        return pt1, pt2


def translation_line_first_side(pt1, pt2, direction='left', move_step=1):
    """

    """
    if direction == 'left':
        pt1 = pt1[0] - move_step, pt1[1]
        pt2 = pt2[0], pt2[1]
        return pt1, pt2
    if direction == 'right':
        pt1 = pt1[0] + move_step, pt1[1]
        pt2 = pt2[0], pt2[1]
        return pt1, pt2
    if direction == 'down':
        pt1 = pt1[0], pt1[1] + move_step
        pt2 = pt2[0], pt2[1]
        return pt1, pt2
    if direction == 'up':
        pt1 = pt1[0], pt1[1] - move_step
        pt2 = pt2[0], pt2[1]
        return pt1, pt2


def translation_line_second_side(pt1, pt2, direction='left', move_step=1):
    """

    """
    if direction == 'left':
        pt1 = pt1[0], pt1[1]
        pt2 = pt2[0] - move_step, pt2[1]
        return pt1, pt2
    if direction == 'right':
        pt1 = pt1[0], pt1[1]
        pt2 = pt2[0] + move_step, pt2[1]
        return pt1, pt2
    if direction == 'down':
        pt1 = pt1[0], pt1[1]
        pt2 = pt2[0], pt2[1] + move_step
        return pt1, pt2
    if direction == 'up':
        pt1 = pt1[0], pt1[1]
        pt2 = pt2[0], pt2[1] - move_step
        return pt1, pt2


if __name__ == '__main__':
    draw_line_from_points(((1, 30), (100, 123)))
