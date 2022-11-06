from PIL import Image
import torch #1.12.1+cu116
from torchvision import transforms
import numpy as np
import matplotlib
import matplotlib.image as img

image_path = './image/'
seg_image_path = './seg_image/'

def masked_image(image,mask):
    image[:,:,0] = mask[0,0,:,:]*255*(1-0.8) + 0.8*image[:,:,0]
    return image

def image_seg(filename):
    image = Image.open(image_path + f'{filename}' + '.jpg')
    w,h = image.size
    image_transforms1 = transforms.Compose([
        transforms.Resize([256, 256]),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.25, 0.25, 0.25])])
    image_transforms2 = transforms.Resize([h, w])

    model_1 = torch.load('road_model.pth', map_location=torch.device('cpu'))
    mask = model_1(image_transforms1(image).unsqueeze(0))

    mask = image_transforms2(mask)
    image = masked_image(np.array(image),mask.detach().numpy())
    matplotlib.image.imsave(seg_image_path + f'{filename}' + '.jpg', image)

#image_seg('C:/Users/65393/Desktop/kfth5g2xk3-1/pothole-mix-no-test-set-20220214/pothole-mix/validation/cnr-road-dataset/images/007.jpg')

