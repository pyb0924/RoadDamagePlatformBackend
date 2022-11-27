import threading

from fastapi import Depends, APIRouter
from fastapi import FastAPI, File, UploadFile, Query
from typing import List, Optional

from api.interceptor import get_db
from model.event.sys_event import *
from common.snow_flake import generate_id

from common.exception import APIException
from common.http_handler import create_response

from service.event import img_service
from common.log import logger

from common.oss import upload_file_oss

event_router = APIRouter(prefix="/event", tags=["养护事件管理"])
image_path = './image/'


# seg_image_path = './seg_image/'
# now_image_path = './'


@event_router.post("", dependencies=[Depends(get_db)])  # 上传图片，建立新养护事件
async def new_event(type: int, longitude: float, latitude: float, address: str, user_id: str, notes: str,
                    file: List[UploadFile] = File(...)):
    try:
        filenamelist = []
        for a in file:
            filename = generate_id()
            path = image_path + f'{filename}.jpg'
            with open(path, 'wb') as f:
                filenamelist.append(filename)
                f.write(await a.read())
                # if type == 0:#如果是用坑或者裂痕
                # imagetest.image_seg(filename)
            # 启动后台线程上传图片至OSS
            threading.Thread(target=upload_file_oss, args=(path, f'{filename}.jpg')).start()
        img_service.new_event(type, longitude, latitude, address, user_id, notes, filenamelist)
        return create_response(200, "新建养护事件成功", {})
    except Exception as e:
        logger.error(e)
        raise APIException(404, "事件信息输入不全或格式错误")


@event_router.get("", dependencies=[Depends(get_db)])  # 按事件的完工条件或位置查询
def search_event(user_id: str = None, type: Optional[List[int]] = Query(None), min_longitude: float = None,
                 max_longitude: float = None, min_latitude: float = None, max_latitude: float = None,
                 address: str = None, status: Optional[List[int]] = Query(None), offset: int = None,
                 limit: int = None):
    try:
        event_list, total = img_service.search_event(user_id, type, min_longitude, max_longitude, min_latitude,
                                                     max_latitude, address, status, offset, limit)
        return create_response(200, "查询事件成功", {"event_list": event_list, "total": total})
    except Exception as e:
        logger.error(e)
        raise APIException(404, "事件信息输入不全或格式错误")


@event_router.put("/{event_id}", dependencies=[Depends(get_db)])  # 修改事件状态
async def update_event(event_id: str, status: int, user_id: str, notes: str, file: List[UploadFile] = File(...)):
    try:
        filenamelist = []
        for a in file:
            img_id = generate_id()
            filenamelist.append(img_id)
            path = image_path + f'{img_id}.jpg'
            with open(path, 'wb') as f:
                f.write(await a.read())
            # 启动后台线程上传图片至OSS
            threading.Thread(target=upload_file_oss, args=(path, f'{img_id}.jpg')).start()
        p = img_service.update_status(event_id, status, user_id, notes, filenamelist)
        if p:
            return create_response(200, "事件状态修改成功", {})
        else:
            raise APIException(404, "非法修改状态")
    except Exception as e:
        logger.error(e)
        raise APIException(404, "事件信息输入不全或格式错误")


@event_router.put("/WithOutImg/{event_id}", dependencies=[Depends(get_db)])  # 修改事件状态
def update_event(event_id: str, status: int, user_id: str, notes: str):
    try:
        p = img_service.update_status(event_id, status, user_id, notes)
        if p:
            return create_response(200, "事件状态修改成功", {})
        else:
            raise APIException(404, "非法修改状态")
    except Exception as e:
        logger.error(e)
        raise APIException(404, "事件信息输入不全或格式错误")


@event_router.get("/log/{log_id}", dependencies=[Depends(get_db)])  # 获得日志对应图片链接
def get_image(log_id: str):
    try:
        img_list = img_service.get_img_by_log(log_id)
        return create_response(200, "图片获取成功", img_list)
    except Exception as e:
        logger.error(e)
        raise APIException(404, "不存在对应日志")


@event_router.get("/{event_id}", dependencies=[Depends(get_db)])
def get_event_by_id(event_id: str):
    try:
        data = vars(Event.get(Event.event_id == event_id))['__data__']
        return create_response(200, "事件信息获取成功", data)
    except Exception as e:
        logger.error(e)
        raise APIException(404, "不存在对应事件")


@event_router.get("/log/{event_id}", dependencies=[Depends(get_db)])
def get_log_by_event(event_id: str):
    try:
        data = img_service.search_log_by_event(event_id)
        return create_response(200, "日志信息获取成功", data)
    except Exception as e:
        logger.error(e)
        raise APIException(404, "事件信息输入不全或格式错误")
