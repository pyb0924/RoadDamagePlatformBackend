import torch
from torch import nn


class conv33(nn.Module):
    def __init__(self,idim,odim):
        super(conv33,self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(idim, odim, 3, 1, 1, bias=False),
            nn.BatchNorm2d(odim),
            nn.LeakyReLU(inplace=True),
            nn.Conv2d(odim, odim, 3, 1, 1, bias=False),
            nn.BatchNorm2d(odim),
            nn.LeakyReLU(inplace=True),
            )
    def forward(self,x):
        x = self.conv(x)
        return x

class Ublock(nn.Module):
    def __init__(self, idim, odim, st):
        super(Ublock,self).__init__()
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
                nn.ConvTranspose2d(odim, odim//2, 2, 2, 0)
                )
        elif st == 'up':
            self.conv = nn.Sequential(
                conv33(idim, odim),
                nn.ConvTranspose2d(odim, odim//2, 2, 2, 0)
                )
        elif st == 'end':
            self.conv = nn.Sequential(
                conv33(idim, odim),
                nn.Conv2d(odim,2,1,1,0),
                nn.Softmax(dim=1)
                )
    def forward(self,x):
        x = self.conv(x)
        return x


class Unet(nn.Module):
    def __init__(self, idim, odim, st, depth=9):
        super(Unet, self).__init__()
        self.depth = depth
        self.idim = idim
        self.odim = odim

        self.blocks = nn.ModuleList([
            Ublock(idim[i], odim[i], st[i])
            for i in range(depth)])

    def forward(self, x):
        y = []
        for i in range(self.depth):
            if i > self.depth // 2:
                x = self.blocks[i](torch.cat((x, y[self.depth - i - 1]), dim=1))
            else:
                x = self.blocks[i](x)
            y.append(x)
        return x