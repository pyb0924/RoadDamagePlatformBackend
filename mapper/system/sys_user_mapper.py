# -*- coding: utf-8 -*-
# @Time    : 10/13/2022 1:50 PM
# @Author  : Zhexian Lin
# @File    : sys_user_mapper.py
# @desc    :

from model.system.sys_user import SysUser


class SysUserMapper:
    def get_user_by_username(self, username):
        """
        以用户名查询用户表
        :param username:
        :return:
        """
        try:
            sys_user = SysUser.get(SysUser.username == username)
        except Exception as e:
            # 用户不存在
            sys_user = None
        return sys_user
