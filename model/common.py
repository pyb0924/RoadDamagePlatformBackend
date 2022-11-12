# -*- coding: utf-8 -*-
# @Time    : 10/13/2022 11:18 AM
# @Author  : Zhexian Lin
# @File    : common.py
# @desc    :

from peewee import *
from datetime import datetime


class BaseModel(Model):
    is_delete = SmallIntegerField(default=0, help_text="0未删除 1已删除")
    create_time = DateTimeField(default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), help_text="0未删除 1已删除")
    update_time = DateTimeField(default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), help_text="0未删除 1已删除")

    def save(self, *args, **kwargs):
        """
        重新save方法，字段更新时，会自动更新update_time字段
        :param args:
        :param kwargs:
        :return:
        """
        self.update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return super(BaseModel, self).save(*args, **kwargs)
