# -*- coding: utf-8 -*-
# @Time    : 10/19/2022 3:00 PM
# @Author  : Zhexian Lin
# @File    : interceptor.py
# @desc    :
from fastapi import Depends, Header

from common.db import db, db_state_default

# 请求前连接数据库
from common.exception import APIException


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


def header_has_authorization(authorization: str = Header(None)):
    if authorization is None:
        raise APIException(401, "token错误")