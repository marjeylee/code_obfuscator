# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     plot_statistic_line
   Description :
   Author :       'li'
   date：          2020/9/7
-------------------------------------------------
   Change Activity:
                   2020/9/7:
-------------------------------------------------
"""
from llib.file_utility.csv_utility import read_csv_file
import numpy as np
from collections import Counter
import seaborn as sns


def get_statistic_line(data, des_path, bins=50, min_range=None, max_range=None):
    """

    :param max_range:
    :param min_range:
    :param data:
    :param des_path:
    :param bins:
    :return:
    """
    data = np.sort(np.array(data))
    total_size = data.size
    if min_range is None:
        min_range = data.min()
    if max_range is None:
        max_range = data.max()
    per_range_size = (max_range - min_range) / bins
    ratio_bins = []
    for d in data:
        ratio = int(d / per_range_size)
        ratio_bins.append(ratio)
    result = Counter(ratio_bins)
    x, y = [], []
    for i in range(bins):
        count = result[i]
        x.append(i * per_range_size)
        y.append(count / total_size)
    ax = sns.lineplot(x=x, y=y)
    hist_fig = ax.get_figure()
    hist_fig.savefig(des_path)


def main():
    content = read_csv_file('res.csv')
    data = []
    for item in content:
        data.append(float(item[2]))
    get_statistic_line(data, 'line.jpg')
    pass


if __name__ == '__main__':
    main()
