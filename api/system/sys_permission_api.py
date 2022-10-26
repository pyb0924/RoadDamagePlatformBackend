# -*- coding: utf-8 -*-
# @Time    : 10/22/2022 11:18 AM
# @Author  : Zhexian Lin
# @File    : sys_permission_api.py
# @desc    :

from fastapi import APIRouter, Depends

from api.interceptor import get_db, has_authorization
from common.http_handler import create_response
from service.system.sys_permission_service import PermissionService

perm_router = APIRouter(prefix="/perm", tags=["权限管理"])
sys_permission_service = PermissionService()


@perm_router.get("", summary="权限列表",
                 dependencies=[Depends(get_db), Depends(has_authorization)])
def get_perm_tree():
    perm_tree = sys_permission_service.get_permission()
    return create_response(200, "请求权限树成功", perm_tree)
