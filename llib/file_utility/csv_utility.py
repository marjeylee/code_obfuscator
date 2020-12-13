# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     csv_utility
   Description :
   Author :       'li'
   date：          2020/1/20
-------------------------------------------------
   Change Activity:
                   2020/1/20:
-------------------------------------------------
"""
import csv
import tqdm


def read_csv_file(csv_file_path, encoding='utf8'):
    """
    :param encoding:
    :param csv_file_path:
    :return:
    """
    bar = tqdm.tqdm()
    all_rows = []
    with open(csv_file_path, mode='r', encoding=encoding)as file:
        reader = csv.reader(file)
        for row in reader:
            bar.update()
            all_rows.append(row)
    return all_rows


def csv_file_to_mapping(csv_path, encoding='gbk'):
    """
    csv content to mapping
    """
    rows = read_csv_file(csv_path, encoding=encoding)
    keys_lst = rows[0]
    content = rows[1:]
    total_row_size = len(content)
    mapping = []
    for i in range(total_row_size):
        row = content[i]
        item = {}
        for index, k in enumerate(keys_lst):
            item[k] = row[index]
        mapping.append(item)
    return mapping


def write_csv_file(csv_file_path, rows, encoding='utf8'):
    """

    :param csv_file_path:
    :param rows:
    :param encoding:
    :return:
    """
    with open(csv_file_path, 'a', encoding=encoding, newline='') as file:
        csv_writer = csv.writer(file, dialect='excel')
        for row in rows:
            csv_writer.writerow(row)
