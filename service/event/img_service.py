import peewee
from model.event.sys_event import *
from common.snow_flake import generate_id
from datetime import datetime
from config import CDN_PREFIX

image_path = './image/'


# seg_image_path = './seg_image/'
# now_image_path = '../'


@db.atomic()
def new_event(type, longitude, latitude, position, user, notes, filenamelist):
    event_id = generate_id()
    log_id = generate_id()

    Event.insert(event_id=event_id,
                 type=type,
                 longitude=longitude,
                 latitude=latitude,
                 address=position,
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
def search_event(user_id=None, type=None, min_longitude=None, max_longitude=None, min_latitude=None, max_latitude=None,
                 position=None, status=None, offset=None, limit=None):
    param = []
    f = True
    if user_id is not None:
        sqlcode = "select distinct event.* from event join log on event.event_id = log.event_id where log.user = %s"

        param.append(user_id)
        f = False
    else:
        sqlcode = "select * from event"

    if type is not None:
        type = [str(x) for x in type]
        ss = ','.join(type)
        if f:
            sqlcode += f" where type in ({ss})"
            f = False
        else:
            sqlcode += f" and type in ({ss})"
        f = False
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
            sqlcode += ' where address like %s'
            f = False
        else:
            sqlcode += ' and address like %s'
        position = f'%{position}%'
        param.append(position)
    if status is not None:
        status = [str(x) for x in status]
        strstatus = ','.join(status)
        if f:
            sqlcode += f" where status in ({strstatus})"
        else:
            sqlcode += f" and status in ({strstatus})"
    total = 0
    if len(param) == 0:
        query = Event.raw(sqlcode).dicts()
    else:
        query = Event.raw(sqlcode, *param).dicts()
    total = len(query)
    event_list = []
    for i in query[(offset-1) * limit:(offset-1) * limit + limit] if offset is not None else query:
        time_sqlcode = 'select datetime from log where event_id = %s order by datetime'
        time_query = Log.raw(time_sqlcode, i['event_id']).dicts()
        i['event_id'] = str(i['event_id'])
        i['create_time'] = str(time_query[0]['datetime'])
        i['update_time'] = str(time_query[-1]['datetime'])
        event_list.append(i)
    return event_list, total


def valid(old_status, status):
    if ((old_status == 4) & (status == 2)) | ((old_status == 1) & (status == 0)):
        return True
    elif old_status == (status - 1):
        return True
    else:
        return False


@db.atomic()
def update_status(event_id, status, user, notes, filenamelist=None):
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
        imagename = f'{i.img_id}.jpg'
        image_list.append(CDN_PREFIX + imagename)
    return image_list


@db.atomic()
def search_event_by_user(user_id):
    sqlcode = 'select event.* from event_user join event on event_user.event_id=event.event_id where user_id=%s'
    query = Event_user.raw(sqlcode, user_id).dicts()
    event_list = []
    for i in query:
        i['event_id'] = str(i['event_id'])
        event_list.append(i)
    return event_list


@db.atomic()
def search_log_by_event(event_id):
    sqlcode = 'select * from log where event_id=%s order by datetime desc'
    query = Log.raw(sqlcode, event_id).dicts()
    log_list = []
    for i in query:
        i["user_id"] = i.pop("user")
        i['datetime'] = str(i['datetime'])
        i['event_id'] = str(i['event_id'])
        i['log_id'] = str(i['log_id'])
        i['user_id'] = str(i['user_id'])
        log_list.append(i)
    return log_list
