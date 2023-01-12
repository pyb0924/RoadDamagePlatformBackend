# -*- coding: utf-8 -*-
# @Time    : 10/19/2022 4:38 PM
# @Author  : Zhexian Lin
# @File    : sys_user_api.py
# @desc    :
import json

from fastapi import APIRouter, Depends, Query

from common.http_handler import create_response
from common.cache import redis_manager
from api.interceptor import get_db, AuthenticationChecker
from common.exception import APIException
from schema.user import UserAdd, UserUpdatePassward, UserEdit

from service.system.sys_user_service import UserService


user_router = APIRouter(prefix="/user", tags=["用户管理"])

user_service = UserService()


@user_router.get("", summary="用户列表",
                 dependencies=[Depends(get_db), Depends(AuthenticationChecker("user"))])
def get_user_list_api(offset: int = Query(default=1, description="偏移量-页码"),
                      limit: int = Query(default=10, description="数据量")):
    users = user_service.get_user_by_offset_limit(offset, limit)
    return create_response(200, "请求用户列表成功", users)


@user_router.get("/{user_id}", summary="用户信息",
                 dependencies=[Depends(get_db), Depends(AuthenticationChecker)])
def get_single_user_info_api(user_id: int):
    user = user_service.get_user_by_user_id(user_id)
    if not user:
        raise APIException(404, f"用户不存在")
    # 每次拉取单个用户信息时，使用redis进行缓存
    redis_manager.set(user["user_id"], json.dumps(str(user["permissions"])))
    return create_response(200, "请求用户信息成功", user)


@user_router.post("", summary="用户新增",
                  dependencies=[Depends(get_db), Depends(AuthenticationChecker("user:add"))])
def add_user_api(user_add: UserAdd):
    user_service.add_user(user_add.username, user_add.password, user_add.permissions)
    return create_response(200, "新增用户成功", {})


@user_router.put("/updateinfo/{user_id}", summary="用户状态、权限变更",
                 dependencies=[Depends(get_db), Depends(AuthenticationChecker("user:edit"))])
def edit_user_api(user_id: str, user_edit: UserEdit):
    user_service.edit_user_status_permissions(user_id, user_edit.is_active, user_edit.permission_ids)
    return create_response(200, "变更用户状态、权限成功", {})


@user_router.put("/updatepwd", summary="用户密码更新",
                 dependencies=[Depends(get_db), Depends(AuthenticationChecker)])
def reset_passward_api(user_update_password: UserUpdatePassward):
    user_service.reset_password(user_update_password.user_id, user_update_password.old_password,
                                user_update_password.password)
    return create_response(200, "密码修改成功", {})


@user_router.delete("/{user_id}", summary="用户删除",
                    dependencies=[Depends(get_db), Depends(AuthenticationChecker("user:delete"))])
def delete_user_api(user_id: int):
    user_service.delete_user(user_id)
    return create_response(200, "用户删除成功", {})
