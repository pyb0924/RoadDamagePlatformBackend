# -*- coding: utf-8 -*-
# @Time    : 10/19/2022 3:44 PM
# @Author  : Zhexian Lin
# @File    : sys_user_role.py
# @desc    :
from peewee import BigIntegerField, CharField

from common.db import db
from common.snow_flake import generate_id
from model.common import BaseModel


class SysUserRole(BaseModel):
    id = BigIntegerField(default=generate_id, null=False, primary_key=True)
    user_id = BigIntegerField(null=False)
    role_id = BigIntegerField(null=False)

    class Meta:
        database = db
        table_name = 'sys_user_role'
