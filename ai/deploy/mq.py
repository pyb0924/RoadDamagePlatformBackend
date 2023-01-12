# -*- coding: utf-8 -*-
# @Time    : 1/11/2023 9:41 PM
# @Author  : Zhexian Lin
# @File    : mq.py
# @desc    :


import pika
from config import *
from road_infer import net_image_to_byte, image_seg
from oss import upload_file_oss

auth = pika.PlainCredentials(MQ_USER, MQ_PASSWORD)
connection = pika.BlockingConnection(pika.ConnectionParameters(MQ_HOST, MQ_PORT, MQ_VIRTUAL_HOST, auth))
channel = connection.channel()
channel.queue_declare(queue='itsm-intelligence', durable=True)


def callback(ch, method, properties, body):
    import json
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(json.loads(body.decode())["image_url"])
    url = json.loads(body.decode())["image_url"]
    byte_image, filename = net_image_to_byte(url)
    image_seg(byte_image, filename)
    upload_file_oss(f"output/{filename}_unet.jpg", f"{filename}_unet.jpg")


if __name__ == '__main__':
    # url = CDN_PREFIX + "1613470219618516992.jpg"
    url = "http://itsmcdn.suphxlin-tech.com/1598522735121031168.jpg"
    byte_image, filename = net_image_to_byte(url)
    image_seg(byte_image, filename)
    upload_file_oss(f"output/{filename}_unet.jpg", f"{filename}_unet.jpg")

    # # 告诉rabbitmq，用callback来接收消息
    # channel.basic_consume('itsm-intelligence', callback)
    # # 开始接收信息，并进入阻塞状态，队列里有信息才会调用callback进行处理
    # channel.start_consuming()