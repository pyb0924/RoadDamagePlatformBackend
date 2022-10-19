# -*- coding: utf-8 -*-
# @Time    : 10/12/2022 9:32 PM
# @Author  : Zhexian Lin
# @File    : main.py
# @desc    :

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn

from api.apis import api_router
from common.exception import APIException
from common.db import database as db

app = FastAPI(title="智慧公路养护管理系统后端", openapi_url="/api/openapi.json")


@app.get("/", tags=["index"])
def index():
    return "智慧公路养护管理系统后端"


# 请求前连接数据库
@app.on_event("startup")
def startup():
    db.connect()


# 请求结束后关闭数据库连接
@app.on_event("shutdown")
def shutdown():
    if not db.is_closed():
        db.close()


# 全局API异常响应格式处理
@app.exception_handler(APIException)
async def api_exception_handler(request: Request, exc: APIException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
    )


# 路由注册
app.include_router(api_router, prefix="/api")

if __name__ == '__main__':
    uvicorn.run(app="main:app", host='127.0.0.1', port=8889, reload=True)
