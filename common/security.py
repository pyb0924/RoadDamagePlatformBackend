# -*- coding: utf-8 -*-
# @Time    : 10/13/2022 1:51 PM
# @Author  : Zhexian Lin
# @File    : security.py
# @desc    :
from fastapi.security import OAuth2PasswordBearer

# token授权依赖项
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")
