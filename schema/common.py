# -*- coding: utf-8 -*-
# @Time    : 10/19/2022 4:33 PM
# @Author  : Zhexian Lin
# @File    : common.py
# @desc    :

from datetime import datetime
from pydantic import BaseModel, Field
from typing import Generic, TypeVar
from pydantic.generics import GenericModel

T = TypeVar("T")


class ReadBase(BaseModel):
    """数据读取的基类"""
    create_time: datetime
    update_time: datetime


class LoginResult(BaseModel):
    """登录响应模型"""

    user_id: int = Field(..., description="用户ID")
    token: str = Field(..., description="token 串")
    token_type: str = Field("Bearer", description="token 类型")


class QueryData(BaseModel):
    """分页查询基础数据"""

    offset: int = 1
    limit: int = 10
