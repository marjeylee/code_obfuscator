# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     xls_utility
   Description :
   Author :       'li'
   date：          2020/5/7
-------------------------------------------------
   Change Activity:
                   2020/5/7:
-------------------------------------------------
"""
import shutil

import xlrd
import xlwt
from llib.file_utility.file_path_utility import combine_file_path


def read_xls_content(xls_path, sheet_index=0):
    """
    read xls content
    :param sheet_index:
    :param xls_path:
    :return:
    """
    data = xlrd.open_workbook(xls_path)
    names = data.sheet_names()
    sheet_name = names[sheet_index]
    table = data.sheet_by_name(sheet_name)
    rows = []
    total_row_size = table.nrows
    total_column_size = table.ncols
    for r in range(total_row_size):
        row = []
        for c in range(total_column_size):
            cell = table.cell(r, c).value
            row.append(cell)
        rows.append(row)
    return rows


def read_xls_content_to_mapping(xls_path, sheet_index=0):
    """
    read xls content
    :param sheet_index:
    :param xls_path:
    :return:
    """
    data = xlrd.open_workbook(xls_path)
    names = data.sheet_names()
    sheet_name = names[sheet_index]
    table = data.sheet_by_name(sheet_name)
    rows = []
    total_row_size = table.nrows
    total_column_size = table.ncols
    for r in range(total_row_size):
        row = []
        for c in range(total_column_size):
            cell = table.cell(r, c).value
            row.append(cell)
        rows.append(row)
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


def write_xls_content(table_name, rows):
    wbk = xlwt.Workbook()
    # 新建一个名为Sheet1的excel sheet。此处的cell_overwrite_ok =True是为了能对同一个单元格重复操作。
    sheet = wbk.add_sheet('Sheet1', cell_overwrite_ok=True)
    # 获取当前日期，得到一个datetime对象如：(2016, 8, 9, 23, 12, 23, 424000)
    # 遍历result中的没个元素。
    for i in range(len(rows)):
        # 对result的每个子元素作遍历，
        for j in range(len(rows[i])):
            # 将每一行的每个元素按行号i,列号j,写入到excel中。
            sheet.write(i, j, rows[i][j])
    # 以传递的name+当前日期作为excel名称保存。
    table_name = table_name.replace(' ', '_')
    wbk.save(combine_file_path('gen/export.xls'))
    shutil.move(combine_file_path('gen/export.xls'), combine_file_path('gen/' + table_name))


def main():
    xls_path = combine_file_path('resource/1.XLS')
    content = read_xls_content(xls_path)


if __name__ == '__main__':
    main()
