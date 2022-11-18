from fastapi import Depends, APIRouter
from fastapi import FastAPI, File, UploadFile
from typing import List

from api.interceptor import get_db
from model.event.sys_event import *
from common.snow_flake import generate_id

from common.exception import APIException
from common.http_handler import create_response

from service.event import img_service
from common.log import logger

event_router = APIRouter(prefix="/event", tags=["养护事件管理"])
image_path = './image/'
seg_image_path = './seg_image/'
now_image_path = './'


@event_router.post("", dependencies=[Depends(get_db)])  # 上传图片，建立新养护事件
async def new_event(type: int, longitude: float, latitude: float, address: str, user: str, notes: str,
                    file: List[UploadFile] = File(...)):
    try:
        filenamelist = []
        for a in file:
            filename = generate_id()
            path = image_path + f'{filename}' + '.jpg'
            with open(path, 'wb') as f:
                filenamelist.append(filename)
                f.write(await a.read())
                # if type == 0:#如果是用坑或者裂痕
                # imagetest.image_seg(filename)
        img_service.new_event(type, longitude, latitude, address, user, notes, filenamelist)
        return create_response(200, "新建养护事件成功", {})
    except Exception as e:
        logger.error(e)
        raise APIException(404, "事件信息输入不全或格式错误")


@event_router.get("", dependencies=[Depends(get_db)])  # 按事件的完工条件或位置查询
async def search_event(type: int = None, min_longitude: float = None, max_longitude: float = None,
                       min_latitude: float = None, max_latitude: float = None, address: str = None,
                       status: int = None):
    try:
        event_list = img_service.search_event(type, min_longitude, max_longitude, min_latitude, max_latitude, address,
                                              status)
        return create_response(200, "查询事件成功", event_list)
    except Exception as e:
        logger.error(e)
        raise APIException(404, "事件信息输入不全或格式错误")


@event_router.put("/{event_id}", dependencies=[Depends(get_db)])  # 修改事件状态
async def update_event(event_id: str, status: int, user: str, notes: str, file: List[UploadFile] = File(...)):
    try:
        filenamelist = []
        for a in file:
            img_id = generate_id()
            filenamelist.append(img_id)
            path = image_path + f'{img_id}' + '.jpg'
            with open(path, 'wb') as f:
                f.write(await a.read())
        p = img_service.update_status(event_id, status, user, notes, filenamelist)
        if p:
            return create_response(200, "事件状态修改成功", {})
        else:
            raise APIException(404, "非法修改状态")
    except Exception as e:
        logger.error(e)
        raise APIException(404, "事件信息输入不全或格式错误")


@event_router.put("/WithOutImg/{event_id}", dependencies=[Depends(get_db)])  # 修改事件状态
async def update_event(event_id: str, status: int, user: str, notes: str):
    try:
        p = img_service.update_status(event_id, status, user, notes)
        if p:
            return create_response(200, "事件状态修改成功", {})
        else:
            raise APIException(404, "非法修改状态")
    except Exception as e:
        logger.error(e)
        raise APIException(404, "事件信息输入不全或格式错误")


@event_router.get("/log/{log_id}", dependencies=[Depends(get_db)])  # 获得日志对应图片链接
async def get_image(log_id: str):
    try:
        img_list = img_service.get_img_by_log(log_id)
        return create_response(200, "图片获取成功", img_list)
    except Exception as e:
        logger.error(e)
        raise APIException(404, "不存在对应日志")


@event_router.get("/{event_id}", dependencies=[Depends(get_db)])
async def get_event_by_id(event_id: str):
    try:
        data = vars(Event.get(Event.event_id == event_id))['__data__']
        return create_response(200, "事件信息获取成功", data)
    except Exception as e:
        logger.error(e)
        raise APIException(404, "不存在对应事件")


@event_router.post("/eventuser", dependencies=[Depends(get_db)])  # 上传图片，建立新养护事件
async def new_event(event_id:str, userlist: List[str]):
    try:
        img_service.new_event_user(event_id, userlist)
        return create_response(200, "新建事件员工成功", {})
    except:
        raise APIException(404, "事件信息输入不全或格式错误")


@event_router.get("/eventuser/{user_id}", dependencies=[Depends(get_db)])
async def get_event_by_user(user_id: str):
    # try:
    data = img_service.search_event_by_user(user_id)
    print(data)
    return create_response(200, "事件信息获取成功", data)