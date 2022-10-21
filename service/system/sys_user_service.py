# -*- coding: utf-8 -*-
# @Time    : 10/13/2022 1:53 PM
# @Author  : Zhexian Lin
# @File    : sys_user_service.py
# @desc    :
from common.exception import APIException
from common.utils import datetime_format
from mapper.system.sys_role_mapper import SysRoleMapper
from mapper.system.sys_user_mapper import SysUserMapper
from model.system.sys_user import SysUser
from common.db import db
from common.log import logger


class UserService:
    sys_user_mapper = SysUserMapper()
    sys_role_mapper = SysRoleMapper()

    def get_user_by_offset_limit(self, offset, limit):
        """
        为API接口提供分页查询用户信息列表
        :param offset:
        :param limit:
        :return:
        """
        skip = (offset - 1) * limit
        user_list = self.sys_user_mapper.get_user_by_offset_limit(skip, limit)

        # 数据库查询数据解析重组
        user_list_dict = dict(user_id=dict())
        for u in user_list:
            if u["user_id"] not in user_list_dict:
                user_list_dict[u["user_id"]] = dict(user_id=str(u['user_id']),
                                                    username=u['username'],
                                                    is_active=u['is_active'],
                                                    roles=[],
                                                    create_time=datetime_format(u['create_time']),
                                                    update_time=datetime_format(u['update_time']))
                if u['role_id']:  # 角色非空时才加入，否则里会在列表中插入None
                    user_list_dict[u["user_id"]]["roles"].append(str(u['role_id']))
            else:
                if u['role_id']:
                    user_list_dict[u["user_id"]]["roles"].append(str(u['role_id']))
        user_list = [v for _, v in user_list_dict.items() if v]

        return user_list

    def get_user_by_user_id(self, user_id: int):
        """
        为API接口提供查询单个用户信息
        :param id:
        :return:
        """
        user_list = self.sys_user_mapper.get_user_by_user_id(user_id)
        if len(user_list) == 0:
            return {}
        # 数据库查询数据解析重组 -- start --
        user_dict = dict(user_id=None, username=None, is_active=None, roles=[])
        for u in user_list:
            user_dict["user_id"] = str(u['user_id'])
            user_dict["username"] = u['username']
            user_dict["is_active"] = u['is_active']
            user_dict["create_time"] = datetime_format(u['create_time'])
            user_dict["update_time"] = datetime_format(u['update_time'])
            user_dict["roles"].append(str(u['role_id']))
        # 数据库查询数据解析重组 -- end --
        return user_dict

    @db.atomic()
    def add_user(self, username, password, roles):
        """
        新增用户方法，前端提供用户名、密码、角色数组

        新增用户保证是原子性行为，若在流程中出现任何异常，都不会更新数据库
        流程：
            1. 检查用户名是否重名，重名则抛出异常，不重名则进入2
            2. 创建用户
            3. 遍历角色数组，先检查角色是否存在，若不存在，直接抛出异常，存在则进入4
            4. 更新sys_user_role_table

        :param username:
        :param password:
        :param roles:
        :return:
        """
        user = self.sys_user_mapper.get_user_by_username(username)
        if user:
            raise APIException(400, f"用户名已存在")

        # 新增用户 -- start --
        new_sys_user = SysUser()
        new_sys_user.username = username
        new_sys_user.convert_pass_to_hash(password)
        self.sys_user_mapper.add_user(new_sys_user)
        # 新增用户 -- end --

        # 依次新增用户角色关联 -- start --
        user_id = new_sys_user.user_id
        for r in roles:
            if not self.sys_role_mapper.get_role_by_id(r):
                raise APIException(400, f"角色不存在")
            self.sys_user_mapper.add_user_role(user_id, r)
        # 依次新增用户角色关联 -- start --

    def reset_password(self, user_id, old_password, password):
        """
        修改密码
        :param user_id:
        :param password:
        :return:
        """
        if self.sys_user_mapper.check_passward_by_user_id(user_id, old_password):
            self.sys_user_mapper.reset_passward_by_user_id(user_id, password)
        else:
            raise APIException(406, f"旧密码错误")
