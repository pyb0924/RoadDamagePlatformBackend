# -*- coding: utf-8 -*-
# @Time    : 10/12/2022 9:32 PM
# @Author  : Zhexian Lin
# @File    : main.py
# @desc    :
import time

from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
import uvicorn
from starlette.routing import Match

from api.apis import api_router
from common.exception import APIException
from common.log import logger

app = FastAPI(title="智慧公路养护管理系统后端",
              openapi_url="/api/openapi.json")


@app.get("/", tags=["index"])
def index():
    return "智慧公路养护管理系统后端"


# 全局API异常响应格式处理
@app.exception_handler(APIException)
async def api_exception_handler(request: Request, exc: APIException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
    )


@app.middleware("http")
async def log_middle(request: Request, call_next):
    logger.debug(f"{request.method} {request.url}")
    routes = request.app.router.routes
    logger.debug("Params:")
    for route in routes:
        match, scope = route.matches(request)
        if match == Match.FULL:
            for name, value in scope["path_params"].items():
                logger.debug(f"\t{name}: {value}")
    logger.debug("Headers:")
    for name, value in request.headers.items():
        logger.debug(f"\t{name}: {value}")

    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.debug(f"completed_in={formatted_process_time}ms status_code={response.status_code}")

    return response

# 路由注册
app.include_router(api_router, prefix="/api")

if __name__ == '__main__':
    uvicorn.run(app="main:app", host='127.0.0.1', port=8889, reload=True, )
