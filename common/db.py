# -*- coding: utf-8 -*-
# @Time    : 10/13/2022 11:15 AM
# @Author  : Zhexian Lin
# @File    : db.py
# @desc    :

from peewee import MySQLDatabase

database = MySQLDatabase("itsm-admin", host='localhost', port=3306, user='root', password='123456', autocommit=True)
