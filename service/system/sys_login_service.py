# -*- coding: utf-8 -*-
# @Time    : 10/13/2022 1:53 PM
# @Author  : Zhexian Lin
# @File    : sys_login_service.py
# @desc    :


from datetime import datetime, timedelta
import jwt
from jwt import PyJWTError

from mapper.system.sys_user_mapper import SysUserMapper


class LoginService:
    sys_user_mapper = SysUserMapper()

    SECRET_KEY = "ShsUP9qIP2Xui2GpXRY6y74v2JSVS0Q2YOXJ22VjwkI"

    ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7

    def create_access_token(self, *, data: dict):
        """
        生成JWT token
        """
        to_encode = data.copy()
        # 设置token过期时间
        expire = datetime.utcnow() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY)
        return encoded_jwt

    def get_user(self, username: str):
        user = self.sys_user_mapper.get_user_by_username(username)
        if not user:
            return None
        return user

    def authenticate_user(self, username: str, password: str):
        """
        登陆认证
        """
        user = self.sys_user_mapper.get_user_by_username(username)
        if not user:
            return None
        if not user.check_password(password):
            return None
        return user
