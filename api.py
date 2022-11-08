from fastapi import APIRouter, Depends
from fastapi import FastAPI, File, UploadFile
from typing import List
import peewee
from sys_event import *
from snow_flake import generate_id
# import imagetest
import img_service
from exception import APIException
from http_handler import create_response
from pydantic import BaseModel
from typing import Union

app = FastAPI()
image_path = './image/'
seg_image_path = './seg_image/'
now_image_path = './'

db = peewee.MySQLDatabase(host='localhost',
                          user='root',
                          password='lmk2000',
                          database='road',
                          charset='utf8')


def get_db():
    try:
        db.connect()
        yield
    finally:
        if not db.is_closed():
            db.close()


@app.post("/event", dependencies=[Depends(get_db)])  # 上传图片，建立新养护事件
async def new_event(type: int, longitude: float, latitude: float, position: str, user: str, notes: str,
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
        img_service.new_event(type, longitude, latitude, position, user, notes, filenamelist)
        return create_response(200, "新建养护事件成功", {})
    except:
        raise APIException(404, "事件信息输入不全或格式错误")


@app.get("/event", dependencies=[Depends(get_db)])  # 按事件的完工条件或位置查询
async def search_event(type: int = None, min_longitude: float = None, max_longitude: float = None,
                       min_latitude: float = None, max_latitude: float = None, position: str = None,
                       status: int = None):
    try:
        event_list = img_service.search_event(type, min_longitude, max_longitude, min_latitude, max_latitude, position,
                                              status)
        return create_response(200, "新建养护事件成功", event_list)
    except:
        raise APIException(404, "事件信息输入不全或格式错误")


@app.put("/event", dependencies=[Depends(get_db)])  # 修改事件状态
async def update_event(event_id: str, status: int, user: str, notes: str, #file:Union[UploadFile, None] = None):
                        file: List[UploadFile] = File(default=None)):
        print(1)
    # try:
        filenamelist = None
        if file[0] is not None:
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
    # except:
    #     raise APIException(404, "事件信息输入不全或格式错误")


@app.get("/event/log/{log_id}", dependencies=[Depends(get_db)])  # 获得日志对应图片链接
async def get_image(log_id: str):
    try:
        img_list = img_service.get_img_by_log(log_id)
        return create_response(200, "图片获取成功", img_list)
    except:
        raise APIException(404, "不存在对应日志")


@app.get("/event/{event_id}", dependencies=[Depends(get_db)])
async def get_event_by_id(event_id: str):
    try:
        data = vars(Event.get(Event.event_id == event_id))['__data__']
        return create_response(200, "事件信息获取成功", data)
    except:
        raise APIException(404, "不存在对应事件")


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='127.0.0.1', port=8000)
