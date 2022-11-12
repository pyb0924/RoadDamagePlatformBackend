# -*- coding: utf-8 -*-
# @Time    : 10/13/2022 1:50 PM
# @Author  : Zhexian Lin
# @File    : sys_user_mapper.py
# @desc    :
from common.exception import APIException
from model.system.sys_permission import SysPermission
from model.system.sys_user import SysUser
from model.system.sys_user_permission import SysUserPermission
from common.log import logger


class SysUserMapper:
    # TODO: 统一Datetime format方法
    def get_user_by_username(self, username):
        """
        以用户名查询用户表，返回用户的对象实例
        :param username:
        :return:
        """
        try:
            sys_user = SysUser().get((SysUser.username == username), (SysUser.is_delete == 0))
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
            sys_user = SysUser.select(SysUser.user_id, SysUser.username, SysUser.is_active,
                                      SysPermission.perm_id,
                                      SysPermission.identifier) \
                .left_outer_join(SysUserPermission, on=(SysUser.user_id == SysUserPermission.user_id)) \
                .left_outer_join(SysPermission, on=(SysUserPermission.perm_id == SysPermission.perm_id)) \
                .where((SysUser.user_id == user_id),
                       (SysUser.is_delete == 0),
                       ((SysUserPermission.is_delete == None) |
                        (SysUserPermission.is_delete == 0)),
                       ((SysPermission.is_delete == None) |
                        (SysPermission.is_delete == 0))) \
                .dicts()
            sys_user = list(sys_user)
        except Exception as e:
            logger.error(e)
            # 用户不存在
            sys_user = []
        return sys_user

    def get_user_by_offset_limit(self, offset, limit):
        try:
            user_list = SysUser.select(SysUser.user_id, SysUser.username, SysUser.is_active, SysUser.create_time,
                                       SysUser.update_time) \
                .where((SysUser.is_delete == 0)) \
                .limit(limit).offset(offset).dicts()
            user_list = list(user_list)
        except Exception as e:
            logger.error(e)
            user_list = []
        return user_list

    def add_user(self, sys_user: SysUser):
        try:
            sys_user.save(force_insert=True)
        except Exception as e:
            sys_user = None
            logger.error(e)
        return sys_user

    def get_user_permission_ids(self, user_id):
        try:
            sys_user_permisson = SysUserPermission().select(SysUserPermission.perm_id).where(
                (SysUserPermission.user_id == user_id) &
                (SysUserPermission.is_delete == 0)).tuples()
            sys_user_permisson = [sup[0] for sup in list(sys_user_permisson)]
            return sys_user_permisson
        except Exception as e:
            logger.error(e)
            return []

    def check_user_permission(self, user_id, perm_id):
        """
        检查用户权限关联项是否已存在
        :param user_id:
        :param role_id:
        :return:
        """
        try:
            sys_user_permisson = SysUserPermission().select().where((SysUserPermission.user_id == user_id),
                                                                    (SysUserPermission.perm_id == perm_id),
                                                                    (SysUserPermission.is_delete == 0)).get()
            if sys_user_permisson:
                return True
        except Exception as e:
            logger.error(e)
            return False

    def add_user_permission(self, user_id, perm_id):
        """
        新增用户权限关联项
        :param user_id:
        :param perm_id:
        :return:
        """
        try:
            sys_user_permission = SysUserPermission(user_id=user_id, perm_id=perm_id)
            sys_user_permission.save(force_insert=True)
        except Exception as e:
            sys_user_permission = None
            logger.error(e)
        return sys_user_permission

    def delete_user_permission(self, user_id, perm_id):
        try:
            sys_user_permission: SysUserPermission = SysUserPermission() \
                .select() \
                .where((SysUserPermission.user_id == user_id),
                       (SysUserPermission.perm_id == perm_id)).get()
            sys_user_permission.delete_instance()
        except Exception as e:
            logger.error(e)
            raise APIException(406, "删除用户权限失败")
        return True

    def update_user(self):
        """
        TODO: 实现用户资料更新，例如权限变更，激活状态变更
        :param sys_user:
        :return:
        """
        pass

    def check_passward_by_user_id(self, user_id, password):
        """
        检查用户ID对应用户的密码与参数密码是否一致
        :param user_id:
        :param password:
        :return:
        """
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
        """
        修改用户ID对应用户的密码
        :param user_id:
        :param password:
        :return:
        """
        try:
            sys_user: SysUser = SysUser().get(SysUser.user_id == user_id)
            sys_user.convert_pass_to_hash(password)
            sys_user.save()
        except Exception as e:
            logger.error(e)
            # 用户不存在
            sys_user = None
        return sys_user


if __name__ == '__main__':
    r = SysUserMapper().get_user_permission_ids(1580216098635255808)
    print(r)