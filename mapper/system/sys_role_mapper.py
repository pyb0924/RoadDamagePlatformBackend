# -*- coding: utf-8 -*-
# @Time    : 10/21/2022 9:20 AM
# @Author  : Zhexian Lin
# @File    : sys_role_mapper.py
# @desc    :

from model.system.sys_role import SysRole
from common.log import logger


class SysRoleMapper:
    def get_role_by_id(self, role_id):
        """
        以用户名查询用户表
        :param username:
        :return:
        """
        try:
            sys_role = SysRole.get(SysRole.role_id == role_id)
        except Exception as e:
            # 用户不存在
            logger.error(e)
            sys_role = None
        return sys_role

    def get_role(self):
        """
        以用户名查询用户表
        :param username:
        :return:
        """
        try:
            sys_role = SysRole.select()
        except Exception as e:
            logger.error(e)
            # 用户不存在
            sys_role = None
        return sys_role

    def add_role(self, sys_role):
        try:
            sys_role.save(force_insert=True)
        except Exception as e:
            logger.error(e)
