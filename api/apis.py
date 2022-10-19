# -*- coding: utf-8 -*-
# @Time    : 10/13/2022 2:35 PM
# @Author  : Zhexian Lin
# @File    : apis.py
# @desc    :


from fastapi import APIRouter

from api.system.login_api import login_router

api_router = APIRouter()

# router注册
api_router.include_router(login_router, tags=["login"])
