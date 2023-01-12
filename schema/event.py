# -*- coding: utf-8 -*-
# @Time    : 1/12/2023 6:29 PM
# @Author  : Zhexian Lin
# @File    : event.py
# @desc    :

from typing import Optional, List
from pydantic import BaseModel


class EventEdit(BaseModel):
    status: int
    user_id: str
    notes: Optional[str] = None
