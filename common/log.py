# -*- coding: utf-8 -*-
# @Time    : 10/21/2022 3:29 PM
# @Author  : Zhexian Lin
# @File    : log.py
# @desc    :
import os
from datetime import datetime

from loguru import logger

if not os.path.exists("logs"):
    os.mkdir("logs")

logger.add(f"logs/{datetime.now().strftime('%Y-%m-%d')}.log", rotation="00:00")
