# -*- coding: utf-8 -*-
# @Time    : 10/19/2022 4:38 PM
# @Author  : Zhexian Lin
# @File    : user_api.py
# @desc    :
from fastapi import APIRouter, Depends, Query

from common.http_handler import create_response
from common.security import oauth2_scheme
from api.interceptor import get_db, header_has_authorization
from common.exception import APIException
from schema.user import UserAdd, UserUpdatePassward

from service.system.sys_user_service import UserService


user_router = APIRouter(prefix="/user", tags=["用户管理"])

user_service = UserService()


@user_router.get("", summary="用户列表",
                 dependencies=[Depends(get_db), Depends(header_has_authorization), Depends(oauth2_scheme)])
async def user_list(offset: int = Query(default=1, description="偏移量-页码"),
                    limit: int = Query(default=10, description="数据量")):
    users = user_service.get_user_by_offset_limit(offset, limit)
    return create_response(200, "请求用户列表成功", users)


@user_router.get("/{user_id}", summary="用户信息",
                 dependencies=[Depends(get_db), Depends(header_has_authorization), Depends(oauth2_scheme)])
async def user_info(user_id: int):
    user = user_service.get_user_by_user_id(user_id)
    if not user:
        raise APIException(404, f"用户不存在")
    return create_response(200, "请求用户信息成功", user)


@user_router.post("", summary="用户新增",
                  dependencies=[Depends(get_db), Depends(header_has_authorization), Depends(oauth2_scheme)])
async def user_info(user_add: UserAdd):
    user_service.add_user(user_add.username, user_add.password, user_add.roles)
    return create_response(200, "新增用户成功", {})


@user_router.put("/updatepwd", summary="用户密码更新",
                 dependencies=[Depends(get_db), Depends(header_has_authorization), Depends(oauth2_scheme)])
async def reset_passward(user_update_password: UserUpdatePassward):
    user_service.reset_password(user_update_password.user_id, user_update_password.old_password,
                                user_update_password.password)
    return create_response(200, "密码修改成功", {})
