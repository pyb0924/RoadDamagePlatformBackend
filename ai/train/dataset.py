from torchvision import transforms
from torch.utils.data import Dataset
import os
from PIL import Image
import torch
import random
import numpy as np

path = '/opt/data/private/lmk/pothole-mix'
t_path = '/opt/data/private/lmk/pothole-mix/training'
v_path = '/opt/data/private/lmk/pothole-mix/validation'


class Segdata(Dataset):
    def __init__(self, dir, test=False, condition_loss = True):
        self.dir = dir
        self.test = test
        self.condition_loss = condition_loss
        self.picdir = os.listdir(self.dir)

        self.images = []
        for i in range(len(self.picdir)):
            l_path = self.dir + '/' + self.picdir[i] + '/' + 'images'
            a = os.listdir(l_path)
            for j in range(len(a)):
                a[j] = l_path + '/' + a[j]
            self.images.extend(a)

        self.masks = []
        for i in range(len(self.picdir)):
            l_path = self.dir + '/' + self.picdir[i] + '/' + 'masks'
            a = os.listdir(l_path)
            for j in range(len(a)):
                a[j] = l_path + '/' + a[j]
            self.masks.extend(a)

    def __len__(self):
        return len(self.images)

    def __getitem__(self, index):
        image_path = self.images[index]
        image = Image.open(image_path).convert('RGB')

        mask_path = self.masks[index]
        mask = Image.open(mask_path).convert('RGB')

        p = random.randint(0, 1)
        if self.test:
            image_transforms = transforms.Compose([
                transforms.Resize([256, 256]),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.25, 0.25, 0.25])]
            )
            mask_transforms = transforms.Compose([
                transforms.ToTensor(),
                transforms.Resize([256, 256])])
        else:
            image_transforms = transforms.Compose([
                transforms.ToTensor(),
                transforms.Resize([256, 256]),
                transforms.RandomHorizontalFlip(p=p),  # 随机水平翻转 0.5概率
                transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.25, 0.25, 0.25])])
            mask_transforms = transforms.Compose([
                transforms.ToTensor(),
                transforms.Resize([256, 256]),
                transforms.RandomHorizontalFlip(p=p),  # 随机水平翻转 0.5概率
            ])

        image = image_transforms(image)
        mask = mask_transforms(mask)  # 第0维红色表示坑，第1维绿色表示裂，第2维啥也没有
        mask[0] = mask[0] + mask[1]
        mask[1] = 1 - mask[0] - mask[1]
        if self.condition_loss:
            label = torch.tensor([torch.max(mask[0]), torch.max(mask[1]), torch.max(mask[2])])
        else:
            label = torch.tensor([1, 1])

        return image, mask[0:2], label
