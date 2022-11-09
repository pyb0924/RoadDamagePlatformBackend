import peewee
from sys_event import *
from snow_flake import generate_id
from datetime import datetime

image_path = './image/'
seg_image_path = './seg_image/'
now_image_path = './'

db = peewee.MySQLDatabase(host='localhost',
                          user='root',
                          password='lmk2000',
                          database='road',
                          charset='utf8')


@db.atomic()
def new_event(type, longitude, latitude, position, user, notes, filenamelist):
    event_id = generate_id()
    log_id = generate_id()

    Event.insert(event_id=event_id,
                 type=type,
                 longitude=longitude,
                 latitude=latitude,
                 position=position,
                 status=1).execute()

    Log.insert(log_id=log_id,
               event_id=event_id,
               datetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
               user=user,
               new_status=1,
               old_status=None,
               notes=notes).execute()

    data = [{
        'img_id': i,
        'log_id': log_id,
        'event_id': event_id
    } for i in filenamelist]
    Img.insert_many(data).execute()
    return '成功'


@db.atomic()
def search_event(type=None, min_longitude=None, max_longitude=None, min_latitude=None, max_latitude=None, position=None,
                 status=None):
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
            sqlcode += ' where position like %s'
            f = False
        else:
            sqlcode += ' and position like %s'
        position = f'%{position}%'
        param.append(position)
    if status is not None:
        if f:
            sqlcode += " where status=%s"
        else:
            sqlcode += " and status=%s"
        param.append(status)

    query = Event.raw(sqlcode, param).dicts()
    event_list = []
    for i in query:
        event_list.append(i)
    return event_list


def valid(old_status, status):
    if ((old_status == 4) & (status == 2)) | ((old_status == 1) & (status == 0)):
        return True
    elif old_status == (status - 1):
        return True
    else:
        return False


@db.atomic()
def update_status(event_id, status, user, notes, filenamelist = None):
    old_status = Event.select().where(Event.event_id == event_id)[0].status
    if valid(old_status, status):
        Event.update(status=status).where(Event.event_id == event_id).execute()
        log_id = generate_id()
        Log.insert(log_id=log_id,
                   event_id=event_id,
                   datetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                   user=user,
                   new_status=status,
                   old_status=old_status,
                   notes=notes).execute()
        if filenamelist is not None:
            data = [{'img_id': i,
                     'log_id': log_id,
                     'event_id': event_id
                     } for i in filenamelist]
            Img.insert_many(data).execute()
        return True
    else:
        return False



@db.atomic()
def get_img_by_log(log_id):
    result = Img.select().where(Img.log_id == log_id)
    image_list = []
    for i in result:
        imagename = str(i.img_id) + '.jpg'
        image_list.append(image_path + imagename)
    return image_list
