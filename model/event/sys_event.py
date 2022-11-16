from peewee import *
from common.db import db


class Event(Model):
    event_id = BigIntegerField(null=False, primary_key=True)
    type = IntegerField(null=False)
    longitude = FloatField(null=False)
    latitude = FloatField(null=False)
    position = CharField(max_length=45, null=False)
    status = IntegerField(null=False)

    class Meta:
        database = db
        table_name = 'event'


class Img(Model):
    img_id = BigIntegerField(null=False, primary_key=True)
    log_id = BigIntegerField(null=False)
    event_id = BigIntegerField(null=False)

    class Meta:
        database = db
        table_name = 'img'


class Log(Model):
    log_id = BigIntegerField(null=False, primary_key=True)
    event_id = BigIntegerField(null=False)
    datetime = DateTimeField(null=False)
    user = BigIntegerField(null=False)
    new_status = IntegerField(null=False)
    old_status = IntegerField(null=True)
    notes = CharField(max_length=200, null=True)

    class Meta:
        database = db
        table_name = 'log'
