# -*- coding: utf-8 -*-
# @Time    : 10/19/2022 3:44 PM
# @Author  : Zhexian Lin
# @File    : sys_permission.py
# @desc    :
from peewee import BigIntegerField, CharField, SmallIntegerField

from common.db import db
from common.snow_flake import generate_id
from model.common import BaseModel


class SysPermission(BaseModel):
    perm_id = BigIntegerField(default=generate_id, null=False, primary_key=True, help_text="权限ID")
    perm_name = CharField(max_length=32, null=False, unique=True, help_text="权限描述")
    type = SmallIntegerField(help_text="权限类型: 0目录 1视图 2按钮 3数据")
    perm_pid = BigIntegerField(help_text="父权限")
    identifier = CharField(null=False, help_text="权限标识")
    client_type = SmallIntegerField(help_text="客户端标识: 0 PC/Web | 1 App")

    class Meta:
        database = db
        table_name = 'sys_permissions'
