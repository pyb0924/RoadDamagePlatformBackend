# -*- coding: utf-8 -*-
# @Time    : 12/8/2022 4:30 PM
# @Author  : Zhexian Lin
# @File    : road_infer.py
# @desc    :
import requests
from PIL import Image
import torch
from torchvision import transforms
import numpy as np
import matplotlib
import matplotlib.image as img
from io import BytesIO

image_path = 'input/'
seg_image_path = 'output/'


def masked_image(image, mask):
    image[:, :, 0] = mask[0, 0, :, :] * 255 * (1 - 0.8) + 0.8 * image[:, :, 0]
    return image


def net_image_to_byte(url):
    try:
        filename = url.split("/")[-1][:-4]
        return BytesIO(requests.get(url).content), filename
    except Exception as e:
        print(e)
        return


def image_seg(byte_image, filename):
    image = Image.open(byte_image)
    w, h = image.size
    image_transforms1 = transforms.Compose([
        transforms.Resize([256, 256]),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.25, 0.25, 0.25])])
    image_transforms2 = transforms.Resize([h, w])

    model_1 = torch.load('road_Unet_label_convmix_2_w2.pth', map_location=torch.device('cpu'))
    mask = model_1(image_transforms1(image).unsqueeze(0))

    mask = image_transforms2(mask)
    image = masked_image(np.array(image), mask.detach().numpy())
    matplotlib.image.imsave(seg_image_path + f'{filename}' + '_unet.jpg', image)


if __name__ == '__main__':
    url = "http://itsmcdn.suphxlin-tech.com/1598522735121031168.jpg"
    byte_image, filename = net_image_to_byte(url)
    image_seg(byte_image, filename)
