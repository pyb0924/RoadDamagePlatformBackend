import model
import dataset
import train
import os
from torch.utils.data import DataLoader, Dataset
import torch
from torch import nn
import torch.optim as optim
from torch.nn import functional as F


class BinaryDiceLoss(nn.Module):
    def __init__(self):
        super(BinaryDiceLoss, self).__init__()

    def forward(self, input, targets):
        # 获取每个批次的大小 N
        # N = targets.size()[0]
        # 平滑变量
        N = 1
        smooth = 1
        # 将宽高 reshape 到同一纬度
        input_flat = input.view(N, -1)
        targets_flat = targets.view(N, -1)

        # 计算交集
        intersection = input_flat * targets_flat
        dice_eff = (2 * intersection.sum(1) + smooth) / (input_flat.sum(1) + targets_flat.sum(1) + smooth)
        # 计算一个批次中平均每张图的损失
        loss = 1 - dice_eff.sum() / N
        return loss


class MultiClassDiceLoss(nn.Module):
    def __init__(self, weight=None, ignore_index=None, **kwargs):
        super(MultiClassDiceLoss, self).__init__()
        self.weight = weight
        self.ignore_index = ignore_index
        self.kwargs = kwargs

    def forward(self, input, target, label):
        """
            input tesor of shape = (N, C, H, W)
            target tensor of shape = (N, C, H, W)
        """
        assert input.shape == target.shape, "predict & target shape do not match"

        binaryDiceLoss = BinaryDiceLoss()
        total_loss = 0

        # 归一化输出
        C = torch.sum(label)

        # 遍历 channel，得到每个类别的二分类 DiceLoss
        for i in range(target.shape[0]):
            for j in range(target.shape[1]):
                if label[i, j] > 0.5:
                    dice_loss = binaryDiceLoss(input[i, j], target[i, j])
                    total_loss += dice_loss

        # 每个类别的平均 dice_loss
        return total_loss / C


base_path = '/opt/data/private/lmk/pothole-mix'  # 2080ti
# base_path = '/root/data/lmk/pothole-mix'#v100
# base_path = 'C:/Users/65393/Desktop/kfth5g2xk3-1/pothole-mix-no-test-set-20220214/pothole-mix'#本地
t_path = base_path + '/training'
v_path = base_path + '/validation'

dataset_s = False

for w in [0.1, 0.5, 1, 2]:
    outlog = base_path + f'/road_Unet_label_convmix_2_w{w}.txt'
    train_data = dataset.Segdata(t_path, condition_loss=dataset_s)
    test_data = dataset.Segdata(v_path, test=True, condition_loss=dataset_s)
    dataloader = {'train': DataLoader(train_data, batch_size=16, shuffle=True, num_workers=8, pin_memory=True),
                  'test': DataLoader(test_data, batch_size=1, shuffle=True, num_workers=8, pin_memory=True)}

    model_ft = model.Unet([3, 64, 128, 256, 512, 1024, 512, 256, 128],
                          [64, 128, 256, 512, 1024, 512, 256, 128, 64],
                          ['start', 'down', 'down', 'down', 'mid', 'up', 'up', 'up', 'end'])

    # criterion = [nn.CrossEntropyLoss(weight = weight1),nn.CrossEntropyLoss(weight = weight2)]
    m_dice_loss = MultiClassDiceLoss()
    # weight1 = torch.tensor([214978928/1871577, 214978928/2039530, 1]).float()
    weight1 = torch.tensor([10 * w, 0.1 * w]).float()
    criterion = [m_dice_loss, nn.CrossEntropyLoss(weight1.to("cuda:7")), nn.L1Loss()]
    optimizer = optim.AdamW(model_ft.parameters(), lr=1e-3)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=20, gamma=0.1)

    model_ft = train.train_model(model_ft, dataloader, criterion, optimizer, scheduler, num_epochs=50, outlog=outlog)
    torch.save(model_ft, base_path + f'/road_Unet_label_convmix_2_w{w}.pth')
