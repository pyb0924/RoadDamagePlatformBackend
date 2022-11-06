from fastapi import APIRouter, Depends
from fastapi import FastAPI, File, UploadFile
from typing import List
#import snowflake.client
import peewee
import imagetest
from snow_flake import generate_id

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

@app.post("/upload",dependencies=[Depends(get_db)])#上传图片，建立新养护事件
async def get_image(type:int,longitude:float,latitude:float,position:str,user:str,notes:str,file: List[UploadFile] = File(...)):
    filenamelist = []
    for a in file:
        filename = generate_id()
        path = image_path + f'{filename}' + '.jpg'
        with open(path,'wb') as f:
            filenamelist.append(filename)
            f.write(await a.read())
            #if type == 0:#如果是用坑或者裂痕
                #imagetest.image_seg(filename)
    event_id = generate_id()
    log_id = generate_id()

    cursor = db.cursor()
    try:
        cursor.execute("insert into event values (%s,%s,%s,%s,%s,%s)",[event_id,type,longitude,latitude,position,0])
        cursor.execute("insert into log values (%s,%s,now(),%s,%s,%s,%s)", [log_id, event_id, user, 1, None, notes])
        cursor.executemany(f"insert into img values (%s,'{log_id}','{event_id}')",filenamelist)
        db.commit()
    except:
        db.rollback()
        return '失败'
    cursor.close()
    return '成功'


@app.get("/search",dependencies=[Depends(get_db)])#按事件的完工条件或位置查询
async def get_image(type:int=None,min_longitude:float=None,max_longitude:float=None,min_latitude:float=None,max_latitude:float=None,position:str=None,status:int=None):
    sqlcode = "select * from event"
    param = []
    f = True
    if type is not None:
        sqlcode += " where type=%s"
        f = False
        param.append(type)
    if min_longitude is not None:
        if f:
            sqlcode += " where longitude>%s and longitude<%s and latitude>%s and latitude<%s"
            f = False
        else:
            sqlcode += " and longitude>%s and longitude<%s and latitude>%s and latitude<%s"
        param.append(min_longitude)
        param.append(max_longitude)
        param.append(min_latitude)
        param.append(max_latitude)
    if position is not None:
        if f:
            sqlcode += " where positon like '%%s%'"
            f = False
        else:
            sqlcode += " and positon like '%%s%'"
        param.append(status)
    if status is not None:
        if f:
            sqlcode += " where status=%s"
        else:
            sqlcode += " and status=%s"
        param.append(status)
    cursor = db.cursor()
    cursor.execute(sqlcode,param)
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result

'''
@app.post("/update_image",dependencies=[Depends(get_db)])#上传当前养护进度图片
async def get_image1(event_id:str,status:int,user:int,notes:str = None, file: List[UploadFile, None] = File(None)):
    filenamelist = []
    for a in file:
        img_id = snowflake.client.get_guid()
        filenamelist.append(img_id)
        path = image_path + f'{img_id}' + '.jpg'
        with open(path,'wb') as f:
            f.write(await a.read())

    cursor = db.cursor()
    try:
        log_id = snowflake.client.get_guid()
        cursor.executemany(f"insert into img values (%s,'{log_id},{event_id}')",filenamelist)
        cursor.execute("insert into log values (%s,%s,now(),%s,%s,%s,%s)", [log_id, event_id, user, status, status, notes])
        db.commit()
    except:
        db.rollback()
        return '失败'
    return "修改成功"
'''

def valid(old_status,status):
    if ((old_status == 4) & (status == 2)) | ((old_status == 1) & (status == 0)):
        return True
    elif old_status == (status-1):
        return True
    else:
        return False

@app.get("/update",dependencies=[Depends(get_db)])#修改事件状态
async def get_image(event_id:str, status:int, user:str, notes:str, file: List[UploadFile] = File(...)):

    cursor = db.cursor()
    cursor.execute("select status from event where event_id=%s",event_id)
    old_status = cursor.fetchall()[0][0]
    cursor.close()
    if valid(old_status,status):
        cursor = db.cursor()
        try:
            cursor.execute("update event set status=%s where event_id=%s", [status, event_id])
            log_id = generate_id()
            cursor.execute("insert into log values (%s,%s,now(),%s,%s,%s,%s)", [log_id,event_id, user, status, old_status,notes])
            if file is not None:
                filenamelist = []
                for a in file:
                    img_id = generate_id()
                    filenamelist.append(img_id)
                    path = image_path + f'{img_id}' + '.jpg'
                    with open(path, 'wb') as f:
                        f.write(await a.read())
                cursor.executemany(f"insert into img values (%s,'{log_id},{event_id}')", filenamelist)
            db.commit()
        except:
            db.rollback()
            return '数据库错误'
        cursor.close()
    else:
        return '非法更改state'

@app.get("/get_img",dependencies=[Depends(get_db)])#获得日志对应图片链接
async def get_image(event_id:str):
    sqlcode = "select img_id from img where log_id=%s"
    cursor = db.cursor()
    cursor.execute(sqlcode,event_id)
    result = cursor.fetchall()
    cursor.close()
    db.close()

    image_list = []

    for i in result:
        print(i)
        imagename = str(i[0]) + '.jpg'
        image_list.append(image_path + imagename)

    return image_list

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app,host='127.0.0.1',port=8000,debug=True)