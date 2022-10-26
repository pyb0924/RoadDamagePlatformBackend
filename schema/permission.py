# -*- coding: utf-8 -*-
# @Time    : 10/24/2022 6:33 PM
# @Author  : Zhexian Lin
# @File    : permission.py
# @desc    :
from pydantic import BaseModel


class PermissionAdd(BaseModel):
    perm_name: str
    type: int
    identifier: str
    perm_pid: str
    client_type: str


class PermissionEdit(BaseModel):
    perm_id: str
    perm_name: str
    type: int
    identifier: str
    perm_pid: str
    client_type: str


class PermissionDelete(BaseModel):
    perm_id: str
