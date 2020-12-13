# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     log_util
   Description :
   Author :       'li'
   date：          2020/3/30
-------------------------------------------------
   Change Activity:
                   2020/3/30:
-------------------------------------------------
"""
import os

from llib.config.config_load import YAMLConfiguration

from llib.log_utility.time_format import TimeFormat
from llib.file_utility.file_path_utility import combine_file_path, create_dir


class LogUtil:

    def __init__(self):
        self.log_path = None
        self.save_log_level = None
        self.log_level_mapping = {'DEBUG': 1, 'INFO': 2, 'WARNING': 3, 'ERROR': 4, 'FATAL': 5}
        self.current_log_level = 1
        self.refresh_config()
        self.current_index = 1

    def log_level_mapping(self):
        """
        level : DEBUG INFO WARNING ERROR FATAL
        """

    def refresh_config(self):
        config = YAMLConfiguration()
        log_dir = config.fetch_value(['LOG', 'LOG_DIR'])
        abs_log_dir = combine_file_path(log_dir)
        create_dir(abs_log_dir)
        log_file_name = config.fetch_value(['LOG', 'LOG_FILE_NAME'])
        self.log_path = os.path.join(abs_log_dir, log_file_name)
        self.save_log_level = config.fetch_value(['LOG', 'LOG_OUTPUT_LEVEL'])
        self.current_log_level = self.log_level_mapping[self.save_log_level]

    def _save_log_to_file(self, log_content):
        """
        save log to file
        :param log_content:
        :return:
        """
        self.current_index = self.current_index + 1
        if self.current_index % 500 == 0:
            self.refresh_config()
        with open(self.log_path, mode='a', encoding='utf8') as file:
            file.write(log_content + '\n')

    def save_log(self, content, level='INFO'):
        """
        save log
        :param content:
        :param level: info  launch error
        :return:
        """
        if level not in self.log_level_mapping:
            return
        if self.log_level_mapping[level] < self.current_log_level:
            return
        current_time = TimeFormat.get_current_time()
        log_content = current_time + ' [' + level + '] ' + content
        self._save_log_to_file(log_content)
        print(log_content)


LOG_UTIL = LogUtil()


def save_log(content, level='INFO'):
    LOG_UTIL.save_log(content, level)


def main():
    log_info = 'dsadsad'
    level = 'INFO'
    save_log(log_info, level)


if __name__ == '__main__':
    main()
