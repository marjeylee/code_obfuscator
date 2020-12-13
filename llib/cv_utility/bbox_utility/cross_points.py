# def cross_point(line1, line2):  # 计算交点函数
#     x1 = line1[0][0]  # 取四点坐标
#     y1 = line1[0][1]
#     x2 = line1[1][0]
#     y2 = line1[1][1]
#     x3 = line2[0][0]
#     y3 = line2[0][1]
#     x4 = line2[1][0]
#     y4 = line2[1][1]
#     k1 = (y2 - y1) * 1.0 / (x2 - x1)  # 计算k1,由于点均为整数，需要进行浮点数转化
#     b1 = y1 * 1.0 - x1 * k1 * 1.0  # 整型转浮点型是关键
#     if (x4 - x3) == 0:  # L2直线斜率不存在操作
#         k2 = None
#         b2 = 0
#     else:
#         k2 = (y4 - y3) * 1.0 / (x4 - x3)  # 斜率存在操作
#         b2 = y3 * 1.0 - x3 * k2 * 1.0
#     if k2 is None:
#         x = x3
#     else:
#         x = (b2 - b1) * 1.0 / (k1 - k2)
#     y = k1 * x * 1.0 + b1 * 1.0
#     return x, y
import numpy as np


def _get_distance(p1, p2):
    return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def cross_point(line1, line2):
    point_is_exist = False
    x = y = 0
    x1 = line1[0][0]  # 取四点坐标
    y1 = line1[0][1]
    x2 = line1[1][0]
    y2 = line1[1][1]
    x3 = line2[0][0]
    y3 = line2[0][1]
    x4 = line2[1][0]
    y4 = line2[1][1]
    if (x2 - x1) == 0:
        k1 = None
    else:
        k1 = (y2 - y1) * 1.0 / (x2 - x1)  # 计算k1,由于点均为整数，需要进行浮点数转化
        b1 = y1 * 1.0 - x1 * k1 * 1.0  # 整型转浮点型是关键

    if (x4 - x3) == 0:  # L2直线斜率不存在
        k2 = None
        b2 = 0
    else:
        k2 = (y4 - y3) * 1.0 / (x4 - x3)  # 斜率存在
        b2 = y3 * 1.0 - x3 * k2 * 1.0

    if k1 is None:
        if not k2 is None:
            x = x1
            y = k2 * x1 + b2
            # point_is_exist = True
    elif k2 is None:
        x = x3
        y = k1 * x3 + b1
    elif not k2 == k1:
        x = (b2 - b1) * 1.0 / (k1 - k2)
        y = k1 * x * 1.0 + b1 * 1.0
        # point_is_exist = True

    return [x, y]


def sort_line_points(start_points, else_points):
    """

    """
    sorter_points = [start_points]
    for point in else_points:
        if len(sorter_points) == 1:
            sorter_points.append(point)
            continue
        for index, saved_point in enumerate(sorter_points):
            if index == 0:
                continue
            save_distance = _get_distance(start_points, saved_point)
            new_distance = _get_distance(start_points, point)
            if save_distance > new_distance:
                sorter_points.insert(index, point)
                break
        sorter_points.append(point)

    return sorter_points


def main():
    line1 = [0, 0, 100, 100]
    line2 = [0, 200, 100, 200]
    print(cross_point(line1, line2))


if __name__ == '__main__':
    main()
