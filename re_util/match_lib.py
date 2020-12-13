# -*- coding: utf-8 -*-
"""
-------------------------------------------------
File Name： match_lib
Description :
Author : 'li'
date： 2020/12/8
-------------------------------------------------
Change Activity:
2020/12/8:
-------------------------------------------------
"""
from llib.file_utility.file_io_utility import read_all_content, read_lines
from llib.file_utility.file_path_utility import get_all_files_under_directory
import re


class MatchLib:
    @staticmethod
    def get_class_name(line):
        """
        get class name
        :param line:
        :return:
        """
        res = re.findall(r"class ([A-Za-z0-9_]+)\(", line)
        if len(res) == 0:
            res = re.findall(r"class ([A-Za-z0-9_]+):", line)
        if len(res) > 0:
            return res[0]
        return None

    @staticmethod
    def get_function_name(line):
        """
        get class name
        :param line:
        :return: (?<=[\*\s\.=\(:\[])+
        """
        res = re.findall(r"def ([A-Za-z_]+[A-Za-z0-9_]*)\(", line)
        if len(res) > 0:
            return res[0]
        return None

    @staticmethod
    def get_variable_name(line):
        """
        get class name
        :param line:
        :return:
        """
        variable_names = []
        re_str = r"(?<=\s)*([A-Za-z0-9_]+)(?=\s*=\s*)"
        for m in re.finditer(re_str, line):
            content_range = m.span()
            variable_names.append(line[content_range[0]:content_range[1]])
        # (?<=\()([a-zA-Z0-9\=\, _\']+)(?=\))  匹配括号内的内容
        # [a-zA-Z0-9_]+\s*= 匹配变量名
        re_str = r"(?<=self\.)([A-Za-z0-9_]+)(?=\s*=\s*)"
        for m in re.finditer(re_str, line):
            content_range = m.span()
            variable_names.append(line[content_range[0]:content_range[1]])
        return variable_names

    @staticmethod
    def get_all_variable_names(content):
        re_str = r'(?<=[\*\s\.=\(:\[])+([A-Za-z]+[\w]*)(?=[\.,=\(\)\s:\}\[\]])+'
        variable_lst = []
        for m in re.finditer(re_str, content):
            content_range = m.span()
            variable_lst.append([content[content_range[0]:content_range[1]], content_range])
        return variable_lst

    @staticmethod
    def get_variable_in_bracket(content):
        re_str = r'(?<=[\(,])+\s*\n*\r*([A-Za-z]+[\w]*)\s*\n*\r*(?=[=])+'
        variable_lst = []
        for m in re.finditer(re_str, content):
            content_range = m.span()
            word = content[content_range[0]:content_range[1]].replace('\t', '').replace('\t', '').replace('\r',
                                                                                                          '').strip()
            variable_lst.append(word)
        return set(variable_lst)

    @staticmethod
    def get_replaceable_name_location(content):
        """
        get class name
        :param content:
        :return:
        """
        variable_names = MatchLib.get_all_variable_names(content)
        re_str = r"\s*([A-Za-z0-9_]*)\s*=\s*[A-Za-z][A-Za-z0-9_]*"
        for m in re.finditer(re_str, content):
            content_range = m.span()
            # print(content[content_range[0]:content_range[1]])

    @staticmethod
    def get_fixed_variable_name(content):
        """
        get class name
        :param content:
        :return:
        """

        re_str = r"\s*([A-Za-z0-9_]*)\s*=\s*[A-Za-z][A-Za-z0-9_]*"
        for m in re.finditer(re_str, content):
            content_range = m.span()
            # print(content[content_range[0]:content_range[1]])

    # if res is None:
    #     return
    # if len(res) > 0:
    #     return res[0]
    # return None


def _main():
    paths = get_all_files_under_directory('C:/Users/Administrator/Desktop/container_and_car_num_release')
    for p in paths:
        if p[-3:] != '.py':
            continue
        content = read_all_content(p)
        class_name = MatchLib.get_all_variable_names(content)
        if class_name is not None:
            print(class_name)


if __name__ == '__main__':
    _main()
