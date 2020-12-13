# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     str_utility
   Description :
   Author :       'li'
   date：          2020/4/2
-------------------------------------------------
   Change Activity:
                   2020/4/2:
-------------------------------------------------
"""
import numpy as np


class StringUtility:
    @staticmethod
    def contain_alphabet(string):
        """
        judge string whether contain num
        :param string:
        :return:
        """
        num = 'QWERTYUIOPASDFGHJKLZXCVBNM'
        for c in string:
            if num.find(c) >= 0:
                return True
        return False

    @staticmethod
    def is_integer(string):
        return string.isdigit()

    @staticmethod
    def contain_number(string):
        """
        judge string whether contain num
        :param string:
        :return:
        """
        num = '0123456789'
        for c in string:
            if num.find(c) >= 0:
                return True
        return False

    @staticmethod
    def get_edit_distance(wrong_str, right_str):
        """
        计算距离
        :parawrong_lenwrong_str:
        :parawrong_lenright_str:
        :return:
        """
        wrong_str = str(wrong_str)
        right_str = str(right_str)
        wrong_len = len(wrong_str)
        right_len = len(right_str)
        distance = np.zeros((wrong_len + 1, right_len + 1))
        for j in range(right_len + 1):
            distance[0][j] = j
        for i in range(wrong_len + 1):
            distance[i][0] = i
        for i in range(1, wrong_len + 1):
            wrong_index = wrong_str[i - 1]
            for j in range(1, right_len + 1):
                right_index = right_str[j - 1]
                if wrong_index == right_index:
                    distance[i][j] = distance[i - 1][j - 1]
                else:
                    distance[i][j] = min(distance[i - 1][j - 1] + 1,
                                         min(distance[i][j - 1] + 1,
                                             distance[i - 1][j] + 1))
        return distance[wrong_len][right_len]


def main():
    a = StringUtility.is_integer('31')
    print(a)
    print('DSADQWRFVDGBER'.isalpha())


if __name__ == '__main__':
    main()
