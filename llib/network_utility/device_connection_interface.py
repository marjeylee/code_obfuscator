# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     device_connection_interface
   Description :
   Author :       'li'
   date：          2020/3/18
-------------------------------------------------
   Change Activity:
                   2020/3/18:
-------------------------------------------------
"""


class DeviceConnectionInterface:
    def __init__(self, host_ip=None, user_name=None, password=None, device_info=None):
        """
        init method
        :param host_ip:
        :param user_name:
        :param password:
        """
        self.host_ip = host_ip
        self.user_name = user_name
        self.password = password
        self.device_info = device_info
        self.is_connection = False

    def close(self):
        """

        :return:
        """
        pass

    def entry_to_super_password(self, super_password):
        pass
