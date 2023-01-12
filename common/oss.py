# -*- coding: utf-8 -*-
# @Time    : 11/20/2022 9:30 AM
# @Author  : Zhexian Lin
# @File    : oss.py
# @desc    :

from qiniu import Auth, put_file, etag
from config import *
from common.mq import produce

# 构建鉴权对象
q = Auth(ACCESS_KEY, SECRET_KEY)


def upload_file_oss(localfile, key):
    """
    上传本地文件至对象存储服务
    :param localfile:  本地文件路径
    :param key:  上传后保存的文件名
    :return:
    """
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(BUCKET_NAME, key, 3600)
    ret, info = put_file(token, key, localfile, version='v2')
    print(info)
    assert ret['key'] == key
    assert ret['hash'] == etag(localfile)
    produce(CDN_PREFIX + key)


if __name__ == '__main__':
    upload_file_oss("../image/IMG_2932.jpg", "IMG_2932.jpg")
