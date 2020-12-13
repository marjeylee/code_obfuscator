# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     telnet_client
   Description :
   Author :       'li'
   date：          2019/12/31
-------------------------------------------------
   Change Activity:
                   2019/12/31:
-------------------------------------------------
"""
import telnetlib
import time

from llib.log_utility.log_util import save_log
from llib.network_utility.device_connection_interface import DeviceConnectionInterface
from llib.network_utility.error_byte_fiter import ERROR_BYTE_FILTER


class TelnetClient(DeviceConnectionInterface):
    def __init__(self, host_ip=None, user_name=None, password=None, device_info=None):
        """
        init method
        :param host_ip:
        :param user_name:
        :param password:
        :param device_info:
        """

        DeviceConnectionInterface.__init__(self, host_ip=host_ip, user_name=user_name,
                                           password=password, device_info=device_info)
        save_log(content='尝试telnet登陆：%s' % self.host_ip, level='DEBUG')
        self.is_connection = self.__create_connection()
        self.connection = self.tn

    def close(self):
        self.tn.close()
        save_log('关闭 %s telnet连接' % self.host_ip, 'DEBUG')

    def input_super_password(self, super_password):
        """

        :return:
        """
        time.sleep(0.2)
        self.tn.read_until('>'.encode('ascii'), timeout=2)
        time.sleep(0.2)
        self.tn.write('enable'.encode('ascii') + b'\n')
        self.tn.read_until(':'.encode('ascii'), timeout=2)
        time.sleep(0.2)
        self.tn.write(super_password.encode('ascii') + b'\n')

    def __create_connection(self):
        """
        create telnet connection
        :return:
        """
        try:
            self.tn = telnetlib.Telnet()
            self.tn.open(self.host_ip, port=23)
            time.sleep(0.2)
            self.tn.read_until(':'.encode('ascii'), timeout=2)
            time.sleep(0.2)
            self.tn.write(self.user_name.encode('ascii') + b'\n')
            time.sleep(0.2)
            self.tn.read_until(":".encode('ascii'), timeout=2)
            time.sleep(0.2)
            self.tn.write(self.password.encode('ascii') + b'\n')
            time.sleep(0.2)
            is_login_success = self.__check_is_login_success()
            if is_login_success:
                save_log(content='telnet 登录%s 成功' % self.host_ip, level='DEBUG')
                return is_login_success
            return False
        except:
            save_log(content='telnet 登录%s失败' % self.host_ip, level='ERROR')
            return False

    def __fetch_execute_result(self):
        """
        fetch execute result
        :return:
        """
        time.sleep(1)
        byte_result = self.tn.read_very_eager()
        exe_result = ERROR_BYTE_FILTER.filter_error_bytes(byte_result)
        return exe_result

    def entry_to_super_password(self, super_password):
        """

        """
        if self.is_connection is False:
            save_log('telnet登录失败，不能执行命令', level='ERROR')
            raise Exception(self.host_ip + 'telnet登录失败，不能执行命令')
        time.sleep(0.5)
        self.tn.write(' '.encode('ascii') + b'\r\n')  # clear and pre-test
        _ = self.__fetch_execute_result()
        time.sleep(0.5)
        self.tn.write('enable'.encode('ascii') + b'\r\n')
        _ = self.__fetch_execute_result()
        self.tn.write(super_password.encode('ascii') + b'\r\n')

    def execute_command(self, command, is_read_first_page=False):
        """
        execute command
        :param is_read_first_page:
        :param command:
        :return:
        """
        if self.is_connection is False:
            save_log('telnet登录失败，不能执行命令', level='ERROR')
            raise Exception(self.host_ip + 'telnet登录失败，不能执行命令')
        time.sleep(0.5)
        self.tn.write(' '.encode('ascii') + b'\r\n')  # clear and pre-test
        _ = self.__fetch_execute_result()
        time.sleep(0.5)
        self.tn.write(command.encode('ascii') + b'\r\n')
        command_result = self.__fetch_execute_result()
        all_result = command_result
        if not is_read_first_page:  # only read first page
            while True:
                self.tn.write(' '.encode('ascii') + b'\r\n')
                command_result = self.__fetch_execute_result()
                filter_command = command_result.replace('\r\n', '').replace(' ', '')

                all_result = all_result + command_result
                # print(command_result)
                if len(filter_command) == 0 or (filter_command[-1] in '>#' and 'More' not in filter_command):
                    break
        all_result = self.__exe_space_one_more_time(all_result)
        # save_log(all_result)
        return all_result

    def __input_blank_space(self):
        self.tn.write(' '.encode('ascii') + b'\r\n')
        time.sleep(1)
        command_result = self.__fetch_execute_result()
        return command_result

    def __check_is_login_success(self):
        """
        check is login success
        :return:
        """
        command_result = self.__input_blank_space().strip()
        if len(command_result) > 0 and (command_result[-1] in '#>'):
            return True
        else:
            command_result = self.__input_blank_space().strip()
        if len(command_result) > 0 and (command_result[-1] in '#>'):
            return True
        return False

    def __exe_space_one_more_time(self, all_result):
        """
        :param all_result:
        :return:
        """
        all_result = all_result + '\n'
        self.tn.write(' '.encode('ascii') + b'\r\n')
        more_result = self.__fetch_execute_result()
        exe_result = all_result + more_result
        return exe_result


def main():
    telnet_client = TelnetClient(host_ip='172.21.9.177', user_name='admin', password='admin@123', device_info=None)
    telnet_client.close()


if __name__ == '__main__':
    main()
