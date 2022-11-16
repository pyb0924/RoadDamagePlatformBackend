# -*- coding: utf-8 -*-
# @Time    : 10/13/2022 2:35 PM
# @Author  : Zhexian Lin
# @File    : apis.py
# @desc    :


from fastapi import APIRouter
from fastapi import Depends

from api.system.sys_user_api import user_router
from common.db import db, db_state_default
from api.system.sys_login_api import login_router
from api.system.sys_permission_api import perm_router
from api.event.event_api import event_router
api_router = APIRouter()

# router注册
api_router.include_router(user_router, tags=["用户管理"])
api_router.include_router(login_router, tags=["登录授权"])
api_router.include_router(perm_router, tags=["权限管理"])
api_router.include_router(event_router, tags=["养护事件管理"])


# 请求前连接数据库
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