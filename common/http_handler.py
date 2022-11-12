# -*- coding: utf-8 -*-
# @Time    : 10/13/2022 2:25 PM
# @Author  : Zhexian Lin
# @File    : http_handler.py
# @desc    :
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


# Http Response结构体
class StatusInfo:
    def __init__(self, code: int, message: str, data: dict = None):
        self.code = code
        self.message = message
        self.data = data

    def get_status_info_dict(self):
        return {
            "code": self.code,
            "message": self.message,
            "data": self.data
        }


# 格式化返回
def create_response(code: int = 200, message: str = '请求成功', data: dict = None):
    return JSONResponse(content=jsonable_encoder(StatusInfo(code=code, message=message, data=data)),
                        media_type="application/json")
