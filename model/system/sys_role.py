# -*- coding: utf-8 -*-
# @Time    : 10/19/2022 3:42 PM
# @Author  : Zhexian Lin
# @File    : sys_role.py
# @desc    :
from peewee import BigIntegerField, CharField

from common.db import db
from common.snow_flake import generate_id
from model.common import BaseModel


class SysRole(BaseModel):
    role_id = BigIntegerField(default=generate_id, null=False, primary_key=True)
    role_name = CharField(max_length=32, null=False)

    class Meta:
        database = db
        table_name = 'sys_roles'


if __name__ == '__main__':
    pass
