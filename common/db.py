# -*- coding: utf-8 -*-
# @Time    : 10/13/2022 11:15 AM
# @Author  : Zhexian Lin
# @File    : db.py
# @desc    :

from contextvars import ContextVar
import peewee
from peewee import MySQLDatabase

db_state_default = {"closed": None, "conn": None, "ctx": None, "transactions": None}
db_state = ContextVar("db_state", default=db_state_default.copy())


class PeeweeConnectionState(peewee._ConnectionState):
    def __init__(self, **kwargs):
        super().__setattr__("_state", db_state)
        super().__init__(**kwargs)

    def __setattr__(self, name, value):
        self._state.get()[name] = value

    def __getattr__(self, name):
        return self._state.get()[name]


db = MySQLDatabase("itsm-admin", host='localhost', port=3306, user='root', password='123456', autocommit=True)

db._state = PeeweeConnectionState()
