import torch
from torch import nn


class convmix(nn.Module):
    def __init__(self, idim, odim):
        super(convmix, self).__init__()
        a = int(odim / 4)
        self.conv1 = nn.Conv2d(idim, a, kernel_size=1, padding=0)
        self.conv3 = nn.Conv2d(idim, a, kernel_size=3, padding=1)
        self.conv5 = nn.Conv2d(idim, a, kernel_size=5, padding=2)
        self.conv7 = nn.Conv2d(idim, a, kernel_size=7, padding=3)

    def forward(self, x):
        x = torch.cat((self.conv1(x), self.conv3(x), self.conv5(x), self.conv7(x)), dim=1)
        return x


class conv33(nn.Module):
    def __init__(self, idim, odim):
        super(conv33, self).__init__()
        self.conv = nn.Sequential(
            convmix(idim, odim),
            nn.BatchNorm2d(odim),
            nn.LeakyReLU(inplace=True),
            convmix(odim, odim),
            nn.BatchNorm2d(odim),
            nn.LeakyReLU(inplace=True),
        )

    def forward(self, x):
        x = self.conv(x)
        return x


# class conv33(nn.Module):
#     def __init__(self, idim, odim):
#         super(conv33, self).__init__()
#         self.conv = nn.Sequential(
#             nn.Conv2d(idim, odim, 3, 1, 1, bias=False),
#             nn.BatchNorm2d(odim),
#             nn.LeakyReLU(inplace=True),
#             nn.Conv2d(odim, odim, 3, 1, 1, bias=False),
#             nn.BatchNorm2d(odim),
#             nn.LeakyReLU(inplace=True),
#         )
#
#     def forward(self, x):
#         x = self.conv(x)
#         return x


class label_block(nn.Module):
    def __init__(self, idim, cla=2, maxidim=512):
        super(label_block, self).__init__()
        self.apool = nn.AvgPool2d(int(16 / 512 * maxidim), stride=1)
        self.mpool = nn.MaxPool2d(2)
        dim = idim
        idimlist = []
        while dim <= maxidim:
            idimlist.append(dim)
            dim = dim * 2
        self.blocks = nn.ModuleList([conv33(int(i), int(i * 2)) for i in idimlist])

        self.out = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(maxidim * 2, cla),
            nn.Softmax(dim=1)
            # nn.Linear(maxidim*2,1)
        )

    def forward(self, x):
        for blk in self.blocks:
            x = self.mpool(x)
            x = blk(x)
        x = self.apool(x)
        x = x.view(x.size(0), -1)
        out = self.out(x)
        return out


class Ublock(nn.Module):
    def __init__(self, idim, odim, st):
        super(Ublock, self).__init__()
        if st == 'start':
            self.conv = nn.Sequential(
                conv33(idim, odim)
            )
        elif st == 'down':
            self.conv = nn.Sequential(
                nn.MaxPool2d(2),
                conv33(idim, odim)
            )
        elif st == 'mid':
            self.conv = nn.Sequential(
                nn.MaxPool2d(2),
                conv33(idim, odim),
                nn.ConvTranspose2d(odim, odim // 2, 2, 2, 0)
            )
        elif st == 'up':
            self.conv = nn.Sequential(
                conv33(idim, odim),
                nn.ConvTranspose2d(odim, odim // 2, 2, 2, 0)
            )
        elif st == 'end':
            self.conv = nn.Sequential(
                conv33(idim, odim),
                nn.Conv2d(odim, 2, 1, 1, 0),

            )

    def forward(self, x):
        x = self.conv(x)
        return x


class Unet(nn.Module):
    def __init__(self, idim, odim, st, depth=9):
        super(Unet, self).__init__()
        self.depth = depth
        self.idim = idim
        self.odim = odim
        self.label_block = label_block(idim=512)
        self.blocks = nn.ModuleList([
            Ublock(idim[i], odim[i], st[i])
            for i in range(depth)])
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        y = []
        for i in range(self.depth):
            if i > self.depth // 2:
                x = self.blocks[i](torch.cat((x, y[self.depth - i - 1]), dim=1))

            else:
                x = self.blocks[i](x)
            y.append(x)
        label = self.label_block(y[3])
        # print(x.shape, label.shape)
        for j in range(label.shape[0]):
            for i in range(label.shape[1]):
                x[j, i, :, :] *= label[j, i]
        x = self.softmax(x)
        return x
