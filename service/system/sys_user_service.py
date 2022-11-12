# -*- coding: utf-8 -*-
# @Time    : 10/13/2022 1:53 PM
# @Author  : Zhexian Lin
# @File    : sys_user_service.py
# @desc    :
from common.exception import APIException
from common.utils import datetime_format
from mapper.system.sys_permission_mapper import SysPermissionMapper
from mapper.system.sys_user_mapper import SysUserMapper
from model.system.sys_user import SysUser
from common.db import db
from common.log import logger


class UserService:
    sys_user_mapper = SysUserMapper()
    sys_user = SysUser()
    sys_permission_mapper = SysPermissionMapper()

    def get_user_by_offset_limit(self, offset, limit):
        """
        为API接口提供分页查询用户信息列表
        :param offset:
        :param limit:
        :return:
        """
        skip = (offset - 1) * limit
        user_list = self.sys_user_mapper.get_user_by_offset_limit(skip, limit)  # 分页查询用户信息
        total_num = self.sys_user.select().where(SysUser.is_delete == 0).count()  # 查询用户总数

        # 数据库查询数据解析重组
        user_list_dict = dict(user_id=dict())
        for u in user_list:
            user_list_dict[u["user_id"]] = dict(user_id=str(u['user_id']),
                                                username=u['username'],
                                                is_active=u['is_active'],
                                                create_time=datetime_format(u['create_time']),
                                                update_time=datetime_format(u['update_time']))
        user_list = [v for _, v in user_list_dict.items() if v]

        return {"total": total_num, "user_list": user_list}

    def get_user_by_user_id(self, user_id: int):
        """
        为API接口提供查询单个用户信息及关联的角色信息
        :param id:
        :return:
        """
        user_list = self.sys_user_mapper.get_user_by_user_id(user_id)
        if len(user_list) == 0:
            return {}
        # 数据库查询数据解析重组 -- start --
        user_dict = dict(user_id=None, username=None, is_active=None, permission_ids=[], permissions=[])
        for u in user_list:
            user_dict["user_id"] = str(u['user_id'])
            user_dict["username"] = u['username']
            user_dict["is_active"] = u['is_active']
            if u['perm_id']:
                user_dict["permission_ids"].append(str(u['perm_id']))
                user_dict["permissions"].append(u['identifier'])
        # 数据库查询数据解析重组 -- end --
        return user_dict

    @db.atomic()
    def add_user(self, username, password, permissions):
        """
        新增用户方法，前端提供用户名、密码、权限ID数组

        新增用户保证是原子性行为，若在流程中出现任何异常，都不会更新数据库
        流程：
            1. 检查用户名是否重名，重名则抛出异常，不重名则进入2
            2. 创建用户
            3. 遍历权限ID数组，先检查权限是否存在，若不存在，直接抛出异常，存在则进入4
            4. 更新sys_user_permission_table

        :param username:
        :param password:
        :param permissions:
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

        # 依次新增用户权限关联 -- start --
        user_id = new_sys_user.user_id
        for p in permissions:
            if not self.sys_permission_mapper.get_permission_by_id(p):
                raise APIException(400, f"权限不存在")
            self.sys_user_mapper.add_user_permission(user_id, p)
        # 依次新增用户权限关联 -- start --

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

    def delete_user(self, user_id):
        try:
            sys_user: SysUser = SysUser.get(SysUser.user_id == user_id)
        except Exception as e:
            logger.error(e)
            raise APIException(404, f"用户不存在")
        try:
            sys_user.delete_instance()
        except Exception as e:
            logger.error(e)
            raise APIException(400, f"用户删除失败")

    @db.atomic()
    def edit_user_status_permissions(self, user_id, is_active, permission_ids):
        try:
            user: SysUser = self.sys_user.select().where((SysUser.user_id == user_id) &
                                                         (SysUser.is_delete == 0)).get()
        except Exception as e:
            logger.error(e)
            raise APIException(404, f"用户不存在")
        user.is_active = is_active
        try:
            user.save()
        except Exception as e:
            logger.error(e)
            raise APIException(406, f"用户状态变更失败")
        current_user_permission_ids = self.sys_user_mapper.get_user_permission_ids(user_id)
        print("current_user_permission_ids:", current_user_permission_ids)
        print("permission_ids:", permission_ids)
        try:
            for perm_id in current_user_permission_ids:
                    # if self.sys_user_mapper.check_user_permission(user_id, perm_id):
                    self.sys_user_mapper.delete_user_permission(user_id, perm_id)

            for perm_id in permission_ids:
                    # if not self.sys_user_mapper.check_user_permission(user_id, perm_id):
                    self.sys_user_mapper.add_user_permission(user_id, perm_id)
        except Exception as e:
            logger.error(e)
            raise APIException(406, f"用户权限变更失败")


if __name__ == '__main__':
    r = UserService().edit_user_status_permissions(1584521618812702720)
    print(r)
