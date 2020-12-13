# -*- coding: utf-8 -*-
"""
-------------------------------------------------
File Name： launch
Description :
Author : 'li'
date： 2020/12/9
-------------------------------------------------
Change Activity:
2020/12/9:
-------------------------------------------------
"""
from exclude.exclude_word import EXCLUDE_WORD_SET
from launch_utility.launch_util import LaunchUtil
from launch_utility.name_mapping import NameMapping
from llib.config.config_load import CONFIGURATION
from llib.file_utility.file_path_utility import get_all_files_under_directory


def obfuscate(py_paths):
    class_names = LaunchUtil.get_class_name(py_paths)
    function_names = LaunchUtil.get_function_name(py_paths)
    variable_names = LaunchUtil.get_variable_name(py_paths)
    names = class_names.union(function_names).union(variable_names)
    name_mapping = NameMapping(names)
    file_and_dir_name = LaunchUtil.get_file_and_dir_name(py_paths)
    exclude_names = EXCLUDE_WORD_SET.union(file_and_dir_name)

    LaunchUtil.obfuscate_code(py_paths, exclude_names, name_mapping)
    print(name_mapping.str_name_mapping)


def _main():
    file_paths = get_all_files_under_directory(CONFIGURATION.fetch_value(['source_code_dir']))
    LaunchUtil.create_destination_dir(file_paths)
    py_paths = LaunchUtil.get_all_py_paths(file_paths)
    obfuscate(py_paths)


if __name__ == '__main__':
    _main()
