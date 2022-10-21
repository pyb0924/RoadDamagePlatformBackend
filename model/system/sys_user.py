# -*- coding: utf-8 -*-
# @Time    : 10/13/2022 11:25 AM
# @Author  : Zhexian Lin
# @File    : sys_user.py
# @desc    :

from model.common import BaseModel
from peewee import BigIntegerField, SmallIntegerField, CharField
from common.snow_flake import generate_id
from common.db import db
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class SysUser(BaseModel):
    user_id = BigIntegerField(default=generate_id, null=False, primary_key=True)
    username = CharField(max_length=32, null=False, unique=True)
    password = CharField(max_length=32, null=False)
    nickname = CharField(max_length=32)
    avatar = CharField(max_length=32)
    email = CharField(max_length=32)
    phone = CharField(max_length=11)
    is_active = SmallIntegerField(default=1)

    class Meta:
        database = db
        table_name = 'sys_users'

    def convert_pass_to_hash(self, password):
        """
        密码加密
        :param password:
        :return:
        """
        self.password = pwd_context.hash(password)
        return self.password

    def check_password(self, password):
        """
        加密密码校验
        :param password:
        :param hashed_password:
        :return:
        """
        return pwd_context.verify(password, self.password)


