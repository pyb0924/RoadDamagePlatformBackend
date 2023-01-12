# -*- coding: utf-8 -*-
# @Time    : 1/11/2023 9:41 PM
# @Author  : Zhexian Lin
# @File    : mq.py
# @desc    :

import pika
from config import *

auth = pika.PlainCredentials(MQ_USER, MQ_PASSWORD)
connection = pika.BlockingConnection(pika.ConnectionParameters(MQ_HOST, MQ_PORT, MQ_VIRTUAL_HOST, auth))
channel = connection.channel()
channel.queue_declare(queue='itsm-intelligence', durable=True)


def produce(url):
    import json
    message = json.dumps({'image_url': url})
    channel.basic_publish(exchange='',
                          routing_key='itsm-intelligence',
                          body=message,
                          properties=pika.BasicProperties(delivery_mode=2, ))
    connection.close()


if __name__ == '__main__':
    produce("http://itsmcdn.suphxlin-tech.com/1598522735121031168.jpg")
