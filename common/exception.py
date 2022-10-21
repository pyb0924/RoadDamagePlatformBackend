# -*- coding: utf-8 -*-
# @Time    : 10/13/2022 2:24 PM
# @Author  : Zhexian Lin
# @File    : exception.py
# @desc    : 统一异常控制

from typing import Any

from fastapi import HTTPException
from common.http_handler import StatusInfo


# 接口异常定义
class APIException(HTTPException):
    """
    """
    status_code: int
    detail: Any

    # 自定义需要返回的信息，在初始化完成并交给父类
    def __init__(self, status_cose=500, message="内部异常", data={}):
        self.status_code = status_cose
        self.detail = StatusInfo(code=status_cose, message=message, data=data).get_status_info_dict()


class FuncException(BaseException):
    def __init__(self, msg):
        super().__init__()
        self.msg = msg

    def __str__(self):
        return '' % self.msg
