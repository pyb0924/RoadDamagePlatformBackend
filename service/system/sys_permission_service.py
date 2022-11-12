# -*- coding: utf-8 -*-
# @Time    : 2022/10/24 15:14
# @Author  : Zhexian Lin
# @File    : sys_permission_service.py
# @desc    :
from common.exception import APIException
from model.system.sys_permission import SysPermission
from schema.permission import PermissionAdd, PermissionEdit, PermissionDelete
from common.log import logger


class PermissionService:
    def get_permission(self):
        """
        返回权限树结构
        :return:
        """
        try:
            sys_permission_list = list(
                SysPermission().select(SysPermission.perm_name.alias("title"), SysPermission.perm_id.alias("key"),
                                       SysPermission.perm_pid).where(
                    SysPermission.is_delete == 0).dicts())
            sys_permission_list_map = {sp["key"]: sp for sp in sys_permission_list}
            arr = []
            for menu in sys_permission_list:
                # 有父级
                menu["key"] = str(menu["key"])
                if mid := menu.get("perm_pid"):
                    # 有子项的情况
                    if result := sys_permission_list_map[mid].get("children"):
                        result.append(menu)
                    else:
                        # 无子项的情况
                        sys_permission_list_map[mid]["children"] = [menu]
                    del menu["perm_pid"]
                else:
                    del menu["perm_pid"]
                    arr.append(menu)
            return arr
        except Exception as e:
            logger.error(e)
            raise APIException()

    def add_permission(self, permission: PermissionAdd):
        sys_permission = SysPermission()
        sys_permission.perm_name = permission.perm_name
        sys_permission.perm_pid = permission.perm_pid
        sys_permission.type = permission.type
        sys_permission.identifier = permission.identifier
        sys_permission.client_type = permission.client_type

        try:
            sys_permission.save(force_insert=True)
        except Exception as e:
            logger.error(e)
            raise APIException(400, message="新增权限失败")

    def edit_permission(self, permission: PermissionEdit):
        try:
            sys_permission = SysPermission().get((SysPermission.perm_id == permission.perm_id),
                                                 (SysPermission.is_delete == 0))
        except Exception as e:
            logger.error(e)
            raise APIException(404, message="权限不存在")

        sys_permission.perm_name = permission.perm_name
        sys_permission.perm_pid = permission.perm_pid
        sys_permission.type = permission.type
        sys_permission.identifier = permission.identifier
        sys_permission.client_type = permission.client_type

        try:
            sys_permission.save()
        except Exception as e:
            logger.error(e)
            raise APIException(400, message="新增权限失败")

    def delete_permission(self, permission: PermissionDelete):
        try:
            sys_permission: SysPermission = SysPermission().get((SysPermission.perm_id == permission.perm_id),
                                                                (SysPermission.is_delete == 0))
        except Exception as e:
            logger.error(e)
            raise APIException(404, message="权限不存在")
        sys_permission.is_delete = 1
        try:
            sys_permission.save()
        except Exception as e:
            logger.error(e)
            raise APIException(400, message="新增权限失败")
