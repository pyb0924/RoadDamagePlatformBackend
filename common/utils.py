# -*- coding: utf-8 -*-
# @Time    : 10/21/2022 10:49 AM
# @Author  : Zhexian Lin
# @File    : utils.py
# @desc    :

from datetime import datetime


def datetime_format(datetime: datetime):
    return datetime.strftime('%Y-%m-%d %H:%M:%S')
