# -*- coding: utf-8 -*-
# @Time    : 10/13/2022 1:50 PM
# @Author  : Zhexian Lin
# @File    : sys_user_mapper.py
# @desc    :

from model.system.sys_user import SysUser
from model.system.sys_user_role import SysUserRole
from common.log import logger


class SysUserMapper:
    # TODO: 统一Datetime format方法
    def get_user_by_username(self, username):
        """
        以用户名查询用户表
        :param username:
        :return:
        """
        try:
            sys_user = SysUser().get(SysUser.username == username)
        except Exception as e:
            logger.error(e)
            # 用户不存在
            sys_user = None
        return sys_user

    def check_passward_by_user_id(self, user_id, password):
        try:
            sys_user: SysUser = SysUser().get(SysUser.user_id == user_id)
            if sys_user.check_password(password):
                return True
            else:
                return False
        except Exception as e:
            logger.error(e)
            # 用户不存在
            return False

    def reset_passward_by_user_id(self, user_id, password):
        try:
            sys_user: SysUser = SysUser().get(SysUser.user_id == user_id)
            sys_user.convert_pass_to_hash(password)
            sys_user.save()
        except Exception as e:
            logger.error(e)
            # 用户不存在
            sys_user = None
        return sys_user

    def get_user_by_user_id(self, user_id):
        """
        以用户名查询用户表
        :param username:
        :return:
        """
        try:
            sys_user = SysUser.select(SysUser.user_id, SysUser.username, SysUser.is_active, SysUserRole.role_id,
                                      SysUser.create_time, SysUser.update_time) \
                .join(SysUserRole, on=(SysUser.user_id == SysUserRole.user_id)) \
                .where((SysUser.user_id == user_id), (SysUser.is_delete == 0), (SysUserRole.is_delete == 0)) \
                .dicts()
            sys_user = list(sys_user)
        except Exception as e:
            logger.error(e)
            # 用户不存在
            sys_user = None
        return sys_user

    def get_user_by_offset_limit(self, offset, limit):
        """
        以用户名查询用户表
        :param username:
        :return:
        """
        try:
            user_list = SysUser.select(SysUser.user_id, SysUser.username, SysUser.is_active, SysUserRole.role_id,
                                       SysUser.create_time, SysUser.update_time) \
                .left_outer_join(SysUserRole, on=(SysUser.user_id == SysUserRole.user_id)) \
                .where((SysUser.is_delete == 0)).offset(offset).limit(limit) \
                .dicts()
            user_list = list(user_list)

        except Exception as e:
            logger.error(e)
            user_list = []
        return user_list

    def add_user(self, sys_user: SysUser):
        try:
            sys_user.save(force_insert=True)
        except Exception as e:
            # 用户名存在
            sys_user = None
            logger.error(e)
        return sys_user

    def add_user_role(self, user_id, role_id):
        try:
            sys_user_role = SysUserRole().create(user_id=user_id, role_id=role_id)
        except Exception as e:
            sys_user_role = None
            logger.error(e)
        return sys_user_role

    def update_user(self, sys_user: SysUser):
        try:
            sys_user.save()
        except Exception as e:
            logger.error(e)
            sys_user = None
        return sys_user


if __name__ == '__main__':
    a = SysUserMapper().get_user_by_user_id(1580216098635255808)
