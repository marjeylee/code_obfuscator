# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     error_byte_fiter
   Description :
   Author :       'li'
   date：          2020/3/12
-------------------------------------------------
   Change Activity:
                   2020/3/12:
-------------------------------------------------
"""


class ErrorByteFilter:
    def __init__(self):
        self.error_byte_list = [b"\x1b[42D                                          \x1b[42D",
                                b'\x08\x08\x08\x08\x08\x08\x08\x08\x08        \x08\x08\x08\x08\x08\x08\x08\x08\x08',
                                b'\x08\x08\x08\x08\x08\x08\x08\x08\x08        \x08\x08\x08\x08\x08\x08\x08\x08\x08',
                                b'\x1b[42D                                          \x1b[42D',
                                b'\x1b[16D                \x1b[16D', b'\x1b[7m--More--\x1b[m',
                                b'\x1b[16D                \x1b[16D',
                                b'\x1b[7m',
                                b'\x1b[m\x1b[K\r\x1b[K',
                                b'\x1b[m\x1b[K',
                                b'\r\x1b[K',
                                b'\x1b[?1h\x1b=\r']
        self.error_byte_list = set(self.error_byte_list)
        self.encoding_type = 'utf8'
        self.error_str_set = self.__get_error_str()

    def filter_error_bytes(self, original_bytes):
        """
        filter error byte
        :param original_bytes:
        :return:
        """
        try:
            original_str = original_bytes.decode(self.encoding_type)
        except:
            original_str = original_bytes.decode('gbk')
        for error_str in self.error_str_set:
            original_str = original_str.replace(error_str, '')
        original_str = original_str.replace('\r\r\n', '\n'). \
            replace('\r\n', '\n').replace('\r', '') \
            .replace('  ---- More ----', '') \
            .replace(' --More-- ', '').replace('---- More ----               ', '') \
            .replace("""---- More ----\n""", '').replace('\r\r\n---- More ----\r\r               \r', '') \
            .replace('\r\r\n---- More ----', '').replace('---- More ----', '').replace('               ', '') \
            .replace('<--- More --->              ', '') \
            .replace('<--- More --->', ' ').replace('\t', '')
        return original_str

    def __get_error_str(self):
        """
        get error str
        :return:
        """
        error_set = set()
        for error_byte in self.error_byte_list:
            error_str = error_byte.decode(self.encoding_type)
            error_set.add(error_str)
        return error_set


ERROR_BYTE_FILTER = ErrorByteFilter()
