# -*- coding: utf-8 -*-
# @Time    : 10/13/2022 2:17 PM
# @Author  : Zhexian Lin
# @File    : login_api.py
# @desc    :

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
import jwt
from jwt import PyJWTError

from common.exception import APIException
from common.http_handler import create_response
from schema.user import UserLogin
from service.system.login_service import LoginService

from common import security
from api.interceptor import get_db, header_has_authorization

login_router = APIRouter()
login_service = LoginService()


@login_router.post("/login", name="用户登陆", dependencies=[Depends(get_db)])
async def login_for_access_token(form_data: UserLogin):
    """
    登录并获取获取token
    """
    user = login_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise APIException(406, f"用户名或密码错误")
    if not user.is_active:
        raise APIException(406, f"{user.username}未激活")
    access_token = login_service.create_access_token(data={"sub": user.username})
    return create_response(200, "登录成功", {"user_id": str(user.user_id), "access_token": access_token.decode(),
                                             "token_type": "bearer"})


@login_router.post("/refresh", name="刷新token", dependencies=[Depends(header_has_authorization)])
async def fresh_token(token: str = Depends(security.oauth2_scheme)):
    """
    刷新token
    :param token:
    :return:
    """
    try:
        payload = jwt.decode(token, login_service.SECRET_KEY)
        username: str = payload.get("sub")
        if username is None:
            raise APIException(406, "token错误")
    except PyJWTError:
        raise APIException(406, "token错误")
    user = login_service.get_user(username)
    if user is None:
        raise APIException(406, "token错误")
    access_token = login_service.create_access_token(data={"sub": user.username})
    return create_response(200, "token刷新成功", {"user_id": str(user.user_id), "access_token": access_token.decode(),
                                                  "token_type": "bearer"})
