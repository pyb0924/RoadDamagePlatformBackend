# -*- coding: utf-8 -*-
# @Time    : 10/19/2022 3:00 PM
# @Author  : Zhexian Lin
# @File    : interceptor.py
# @desc    :
from fastapi import Depends
import json
import jwt
from jwt import PyJWTError

from common.db import db, db_state_default
from common.cache import redis_manager
from model.system.sys_user import SysUser

# 请求前连接数据库
from common.exception import APIException
from common.security import oauth2_scheme


async def reset_db_state():
    db._state._state.set(db_state_default.copy())
    db._state.reset()


def get_db(db_state=Depends(reset_db_state)):
    try:
        db.connect()
        yield
    finally:
        if not db.is_closed():
            db.close()


class AuthenticationChecker:
    """
    授权检查依赖对象：对依赖接口进行身份认证和权限判断

    """
    def __init__(self, identifier: str = None, db=Depends(get_db), token: str = Depends(oauth2_scheme)):
        self.db = db
        self.token = token
        self.identifier = identifier

    def __call__(self, token: str = Depends(oauth2_scheme)):
        # 身份认证：
        # 保证请求携带token，并满足：
        # 1. token未过期
        # 2. token的payload能解析出登录用户
        try:
            payload = jwt.decode(token, "ShsUP9qIP2Xui2GpXRY6y74v2JSVS0Q2YOXJ22VjwkI")
            username: str = payload.get("sub")
            if username is None:
                raise APIException(406, "token错误")
        except PyJWTError:
            raise APIException(406, "token错误")
        user: SysUser = SysUser().get(SysUser.username == username)
        if user is None:
            raise APIException(406, "token错误")

        # identifier不为None时, 检查该用户是否拥有该权限
        if self.identifier is not None:
            perm_list = redis_manager.get(user.user_id)
            perm_list = json.loads(perm_list)
            if self.identifier not in perm_list:
                raise APIException(406, "无权访问")
        return user
