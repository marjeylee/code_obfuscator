# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     ssh_connection
   Description :
   Author :       'li'
   date：          2020/1/14
-------------------------------------------------
   Change Activity:
                   2020/1/14:
-------------------------------------------------
"""
import time

import paramiko

from llib.log_utility.log_util import save_log
from llib.network_utility.device_connection_interface import DeviceConnectionInterface
from llib.network_utility.error_byte_fiter import ERROR_BYTE_FILTER


class SSHClient(DeviceConnectionInterface):
    """
    SSHClient
    """

    def __init__(self, host_ip=None, user_name=None, password=None, device_info=None):
        """

        :param host_ip:
        :param user_name:
        :param password:
        :param device_info:
        """
        DeviceConnectionInterface.__init__(self, host_ip=host_ip, user_name=user_name,
                                           password=password, device_info=device_info)
        self.connection = self.init_connection()
        self.is_connection = self.connection is not None
        if self.is_connection:
            self.channel = self.connection.invoke_shell()
        else:
            self.connection = None

    def close(self):
        if self.is_connection:
            self.connection.close()
        save_log('关闭%s连接' % self.host_ip, 'DEBUG')

    def init_connection(self):
        """
        init connection
        :return:
        """
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            save_log('尝试登录SSH，IP:%s' % self.host_ip, 'DEBUG')
            ssh.connect(self.host_ip, 22, self.user_name, self.password,
                        allow_agent=False, look_for_keys=False, timeout=5)
            if ssh is not None:
                save_log('SSH登录IP:%s成功' % self.host_ip, 'DEBUG')
                return ssh
            save_log('SSH登录IP:%s失败' % self.host_ip, 'ERROR')
            return None
        except Exception as e:
            print(e)
            save_log('SSH登录IP:%s失败' % self.host_ip, 'ERROR')
            return None

    @staticmethod
    def __fetch_execute_result(channel):
        """
        fetch execute result
        :param channel:
        :return:
        """
        time.sleep(1)
        exe_result = ''
        while channel.recv_ready():
            lines = channel.recv(1024)
            lines = ERROR_BYTE_FILTER.filter_error_bytes(lines)
            exe_result = exe_result + lines
        return exe_result

    def execute_command(self, command, is_read_first_page=False):
        """
        execute command
        :param is_read_first_page:
        :param command:
        :return:
        """
        if self.connection is None:
            save_log('IP:%s,SSH登录失败,不能执行命令' % self.host_ip, 'ERROR')
            raise Exception(self.host_ip + 'SSH登录失败，不能执行命令')
        time.sleep(0.5)
        self.channel.send(' ' + '\r\n')
        _ = self.__fetch_execute_result(self.channel)
        time.sleep(0.5)
        self.channel.send(command + '\r\n')
        exe_result = self.__fetch_execute_result(self.channel)
        self.channel.send(' ')
        more_result = self.__fetch_execute_result(self.channel)
        exe_result = exe_result + more_result
        last_res = ''
        if not is_read_first_page:
            while True:
                if not self.check_is_output_finish(exe_result):
                    exe_result = exe_result + '\n'
                    self.channel.send(' ')
                    more_result = self.__fetch_execute_result(self.channel)
                    if more_result == last_res:
                        break
                    last_res = more_result
                    exe_result = exe_result + more_result
                else:
                    break
        exe_result = self.__exe_space_one_more_time(exe_result)
        return exe_result

    def input_super_password(self, super_password):
        """

        :return:
        """
        pass

    def __exe_space_one_more_time(self, exe_result):

        """
        :param exe_result:
        :return:
        """
        exe_result = exe_result + '\n'
        self.channel.send(' ')
        self.channel.send('\r\n')
        more_result = self.__fetch_execute_result(self.channel)
        exe_result = exe_result + more_result
        return exe_result

    @staticmethod
    def check_is_output_finish(exe_result):
        """

        :param exe_result:
        :return:
        """
        if len(exe_result) > 30:
            return False
        tmp_str = exe_result.replace(' ', '').replace('\r', '').replace('\n', '')
        if len(tmp_str) == 0 or tmp_str[-1] in '>#':
            return True
        return False


if __name__ == '__main__':
    cl = SSHClient('188.253.0.67', 'root', 'Root188.253.0.66')
    res = cl.execute_command('ll ')
    print(res)
