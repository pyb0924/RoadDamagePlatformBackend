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
    perm_id = BigIntegerField(default=generate_id, null=False, primary_key=True)
    perm_name = CharField(max_length=32, null=False, unique=True)
    type = SmallIntegerField(null=False)
    perm_pid = BigIntegerField()
    component = CharField()
    identifier = CharField()
    api = CharField()
    method = CharField()
    client_type = SmallIntegerField()

    class Meta:
        database = db
        table_name = 'sys_permissions'
