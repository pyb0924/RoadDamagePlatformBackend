# -*- coding: utf-8 -*-
# @Time    : 2022/11/7 20:23
# @Author  : Zhexian Lin
# @File    : cache.py
# @desc    :

import redis as r
from config import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_DB_NB

redis_pool = r.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=REDIS_DB_NB)
redis_manager = r.Redis(connection_pool=redis_pool)
