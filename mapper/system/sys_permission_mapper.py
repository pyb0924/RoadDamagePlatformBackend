# -*- coding: utf-8 -*-
# @Time    : 10/24/2022 11:23 AM
# @Author  : Zhexian Lin
# @File    : sys_permission_api.py
# @desc    :


from model.system.sys_permission import SysPermission
from common.log import logger

class SysPermissionMapper:
    def get_permission_by_id(self, perm_id):
        try:
            sys_role = SysPermission.get((SysPermission.perm_id == perm_id), (SysPermission.is_delete == 0))
        except Exception as e:
            logger.error(e)
            sys_role = None
        return sys_role

    def get_permission_by_offset_limit(self, offset, limit):
        try:
            sys_permission_list = SysPermission.select().where(SysPermission.is_delete == 0).offset(offset).limit(limit) \
                .dicts()
            sys_permission_list = list(sys_permission_list)

        except Exception as e:
            logger.error(e)
            sys_permission_list = []
        return sys_permission_list

    def add_permission(self, sys_permission):
        try:
            sys_permission.save(force_insert=True)
        except Exception as e:
            logger.error(e)


if __name__ == '__main__':
    sys_permission = SysPermission()
    sys_permission.perm_name = "权限删除"
    sys_permission.type = 2
    sys_permission.identifier = "perm:delete"
    sys_permission.perm_pid = 1584446902865367040
    sys_permission.client_type = "0"
    sys_permission.save(force_insert=True)