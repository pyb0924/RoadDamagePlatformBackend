# -*- coding: utf-8 -*-
# @Time    : 10/13/2022 11:15 AM
# @Author  : Zhexian Lin
# @File    : db.py
# @desc    :

from contextvars import ContextVar
import peewee
from config import *
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


db = MySQLDatabase(DB_NAME, host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, autocommit=True)

db._state = PeeweeConnectionState()