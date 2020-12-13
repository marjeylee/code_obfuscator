# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     device_connection
   Description :
   Author :       'li'
   date：          2020/1/20
-------------------------------------------------
   Change Activity:
                   2020/1/20:
-------------------------------------------------
"""
from llib.network_utility.ssh_connection import SSHClient
from llib.network_utility.telnet_client import TelnetClient


class DeviceConnectionClient:
    def __init__(self, ip=None, username=None,
                 password=None,
                 connection_type='telnet',
                 device_type='huawei',
                 device_hardware_version=None,
                 device_info=None
                 ):
        """
        init method
        :param username:
        :param password:
        :param connection_type:telnet,ssh
        :param device_type:
        :param device_hardware_version:
        """
        self.ip = ip
        self.username = username
        self.password = password
        self.device_info = device_info
        self.connection_type = connection_type
        self.device_type = device_type
        self.device_hardware_version = device_hardware_version
        self.connection = self.__try_login_device()

    def is_connected(self):
        """
        check is connected
        :return:
        """
        return self.connection.is_connection

    def execute_command(self, command, is_read_first_page=False):
        """

        :param command:
        :param is_read_first_page:
        :return:
        """
        return self.connection.execute_command(command, is_read_first_page=is_read_first_page)

    def __try_login_device(self):
        """
        try login
        :return:
        """

        if 'SSH' == self.connection_type.strip():
            connection = SSHClient(self.ip, self.username, self.password, self.device_info)
        else:
            connection = TelnetClient(self.ip, self.username, self.password, self.device_info)
        self.connection = connection
        # if '防火墙' in self.device_info['DC名称'] and self.device_info['设备厂商'] == 'Cisco':
        #     super_password = self.device_info['超级密码']
        #     self.input_super_password(super_password)
        return connection

    def close(self):
        """
        close connection
        :return:
        """

        self.connection.close()
        self.connection.is_connection = False

    def input_super_password(self, super_password):
        """

        :param super_password:
        :return:
        """
        self.connection.input_super_password(super_password)
