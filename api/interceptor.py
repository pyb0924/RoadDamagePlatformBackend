# -*- coding: utf-8 -*-
# @Time    : 10/19/2022 3:00 PM
# @Author  : Zhexian Lin
# @File    : interceptor.py
# @desc    :
from fastapi import Depends
import jwt
from jwt import PyJWTError

from common.db import db, db_state_default
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


def has_authorization(db=Depends(get_db), token: str = Depends(oauth2_scheme), ):
    try:
        payload = jwt.decode(token, "ShsUP9qIP2Xui2GpXRY6y74v2JSVS0Q2YOXJ22VjwkI")
        username: str = payload.get("sub")
        if username is None:
            raise APIException(406, "token错误")
    except PyJWTError:
        raise APIException(406, "token错误")
    user = SysUser().get(SysUser.username == username)
    if user is None:
        raise APIException(406, "token错误")
    return user
