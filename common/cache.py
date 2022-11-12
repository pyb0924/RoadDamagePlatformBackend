# -*- coding: utf-8 -*-
# @Time    : 2022/11/7 20:23
# @Author  : Zhexian Lin
# @File    : cache.py
# @desc    :

import redis as r

redis_pool = r.ConnectionPool(host='127.0.0.1', port=6379, password='', db=0)
redis_manager = r.Redis(connection_pool=redis_pool)
