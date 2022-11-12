# -*- coding: utf-8 -*-
# @Time    : 10/12/2022 4:01 PM
# @Author  : Zhexian Lin
# @File    : user.py
# @desc    :
from typing import Optional, List
from pydantic import BaseModel, Field
from schema.common import QueryData, ReadBase


class UserLogin(BaseModel):
    username: str
    password: str


class UserAdd(BaseModel):
    username: str
    password: str
    permissions: List[int]


class UserEdit(BaseModel):
    is_active: int
    permission_ids: List[str]


class UserUpdatePassward(BaseModel):
    user_id: str
    old_password: str
    password: str
