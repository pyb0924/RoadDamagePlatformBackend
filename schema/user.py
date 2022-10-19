# -*- coding: utf-8 -*-
# @Time    : 10/12/2022 4:01 PM
# @Author  : Zhexian Lin
# @File    : user.py
# @desc    :


from pydantic import BaseModel


class Token(BaseModel):
    """
    token schema
    """
    access_token: str
    token_type: str
