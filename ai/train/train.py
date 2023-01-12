from torchvision import transforms
from torch.utils.data import DataLoader, Dataset
import os
import numpy as np
from PIL import Image
import torch
from torch import nn
import random
import torch.optim as optim
import time
from torch.nn import functional as F


def writelog(txt, filepath, w=True):
    print(txt)
    if w:
        with open(filepath, "a") as f:
            f.write(str(txt) + '\n')


def eva_cal(pre, mask, smooth=0.0001):
    TP = torch.sum((pre == 1) & (mask == 1)) / 65536
    TN = torch.sum((pre == 0) & (mask == 0)) / 65536
    FP = torch.sum((pre == 1) & (mask == 0)) / 65536
    FN = torch.sum((pre == 0) & (mask == 1)) / 65536
    acc = (TP + TN) / (TP + TN + FP + FN)
    recall = (TP + smooth) / (TP + FN + smooth)
    iou = (TP + smooth) / (TP + FP + FN + +smooth)
    dice = (2 * TP + smooth) / (2 * TP + FP + FN + +smooth)
    eva = torch.tensor([acc, recall, dice, iou])
    return eva


def train_model(model,
                dataloader,
                criterion,
                optimizer,
                scheduler,
                num_epochs,
                outlog):
    train_on_gpu = torch.cuda.is_available()
    if not train_on_gpu:
        print('CUDA is not available.  Training on CPU ...')
    else:
        print('CUDA is available!  Training on GPU ...')
    device = torch.device("cuda:7" if torch.cuda.is_available() else "cpu")
    print(device)
    model.to(device)
    for epoch in range(num_epochs):
        writelog('Epoch {}/{}'.format(epoch, num_epochs - 1), outlog)
        writelog('-' * 10, outlog)
        # 训练和验证
        for phase in ['train', 'test']:
            if phase == 'train':
                model.train()  # 训练
            else:
                model.eval()  # 验证
            running_loss = 0.0
            running_eva = 0.0
            imgnum = 0
            class_ratio = torch.tensor([0, 0, 0])
            # 把数据都取个遍
            for image, mask, label in dataloader[phase]:
                if epoch == 0:
                    for i in range(2):
                        class_ratio[i] = class_ratio[i] + torch.sum(mask[:, i, :, :])
                # print(1)
                image = image.to(device)
                mask = mask.to(device)
                label = label.to(device)
                # 清零
                optimizer.zero_grad()
                # 只有训练的时候计算和更新梯度
                with torch.set_grad_enabled(phase == 'train'):
                    pre_mask = model(image)

                    loss = criterion[0](pre_mask, mask, label) + criterion[1](pre_mask, mask)
                    if phase == 'train':
                        loss.backward()
                        optimizer.step()
                # 计算损失
                running_loss += loss.detach() * image.size(0)
                if phase == 'test':
                    argmax_pre_mask = torch.argmax(pre_mask, dim=1)
                    pre_mask0 = torch.where(argmax_pre_mask == 0, 1, 0)
                    pre_mask1 = torch.where(argmax_pre_mask == 1, 1, 0)

                    eva0 = eva_cal(pre_mask0[0, :, :].float().round(), mask[0, 0, :, :].round())
                    eva1 = eva_cal(pre_mask1[0, :, :].float().round(), mask[0, 1, :, :].round())

                    eva = eva0 + eva1
                    running_eva += eva / 2
                imgnum += image.size(0)
            if epoch == 0:
                writelog(f'class_ratio:{class_ratio}', outlog)
            epoch_loss = running_loss / imgnum
            writelog('{} Loss:{:.4f}'.format(phase, epoch_loss), outlog)
            if phase == 'test':
                epoch_eva = running_eva / imgnum
                writelog('     acc    recall    dice    iou', outlog, w=True)
                writelog(epoch_eva, outlog, w=True)
        scheduler.step()
        writelog('', outlog)
    return model
