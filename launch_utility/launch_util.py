# -*- coding: utf-8 -*-
"""
-------------------------------------------------
File Name： launch_util
Description :
Author : 'li'
date： 2020/12/9
-------------------------------------------------
Change Activity:
2020/12/9:
-------------------------------------------------
"""
import os
import shutil

from llib.config.config_load import CONFIGURATION
from llib.file_utility.file_io_utility import read_lines, read_all_content
from llib.file_utility.file_path_utility import create_dir
from re_util.match_lib import MatchLib


class LaunchUtil:
    @staticmethod
    def get_all_py_paths(path):
        py_paths = []
        for p in path:
            if '.py' == p[-3:]:
                py_paths.append(p)
            else:
                try:
                    new_path = p.replace(CONFIGURATION.fetch_value(['source_code_dir']),
                                         CONFIGURATION.fetch_value(['destination_code_dir']))
                    shutil.copy(p, new_path)
                except Exception as e:
                    print(e)
        return py_paths

    @staticmethod
    def get_class_name(py_paths):
        class_name_set = set()
        for p in py_paths:
            lines = read_lines(p)
            for line in lines:
                class_name = MatchLib.get_class_name(line)
                if class_name is not None:
                    class_name_set.add(class_name)
        return class_name_set

    @staticmethod
    def get_function_name(py_paths):
        class_name_set = set()
        for p in py_paths:
            lines = read_lines(p)
            for line in lines:
                class_name = MatchLib.get_function_name(line)
                if class_name is not None:
                    class_name_set.add(class_name)
        return class_name_set

    @staticmethod
    def get_variable_name(py_paths):
        class_name_set = []
        for p in py_paths:
            lines = read_lines(p)
            for line in lines:
                class_name = MatchLib.get_variable_name(line)
                if len(class_name) > 0 and class_name is not None:
                    class_name_set = class_name_set + class_name
        class_name_set = set(class_name_set)
        return class_name_set

    @staticmethod
    def create_destination_dir(file_paths):
        for path in file_paths:
            tmp_dir, _ = os.path.split(path)
            tmp_dir = tmp_dir.replace(CONFIGURATION.fetch_value(['source_code_dir']),
                                      CONFIGURATION.fetch_value(['destination_code_dir']))
            create_dir(tmp_dir)

    @staticmethod
    def obfuscate_code(py_paths, exclude_names_set, name_mapping):
        """

        :return:
        """
        variable_in_bracket_set = set()
        for path in py_paths:
            content = read_all_content(path)
            variable_in_bracket = MatchLib.get_variable_in_bracket(content)
            variable_in_bracket_set = variable_in_bracket_set.union(variable_in_bracket)
        for path in py_paths:
            content = read_all_content(path)
            if 'mix_container_recognize' in path and 'common' in path and '__init_' in path:
                print(path)
            variable_lst = MatchLib.get_all_variable_names(content)
            name_uuid_mapping = name_mapping.name_str_mapping
            new_content = ''
            current_index = 0
            for key, location in variable_lst:
                if key not in name_uuid_mapping or key in exclude_names_set:
                    continue
                if key in variable_in_bracket_set:
                    continue
                new_content = new_content + content[current_index:location[0]] + name_uuid_mapping[key]
                current_index = location[1]
            new_content = new_content + content[current_index:]
            new_path = path.replace(CONFIGURATION.fetch_value(['source_code_dir']),
                                    CONFIGURATION.fetch_value(['destination_code_dir']))
            with open(new_path, mode='w', encoding='utf8') as file:
                file.write(new_content)

    @staticmethod
    def get_file_and_dir_name(py_paths):
        file_names = []
        for p in py_paths:
            while True:
                p, file_name = os.path.split(p)
                if len(file_name) == 0:
                    break
                file_name = file_name.replace('.py', '')
                file_names.append(file_name)
                p, file_name = os.path.split(p)
                if len(file_name) == 0:
                    break
                file_names.append(file_name)
        return set(file_names)
