from torch.utils.data.dataset import Dataset
import os
import numpy as np
import random
from PIL import Image, ImageEnhance
import torch

class SingleTestDataset(Dataset):

    def __init__(self, trainsetfile, mean, std):
        super(SingleTestDataset, self).__init__()
        # self.trainsetFile = []
        # self.aimsetFile = []

        self.mean = mean
        self.std = std
        self.trainsetFile = trainsetfile


    def normalise(self, x, mean=(0.4914, 0.4822, 0.4465), std=(0.2471, 0.2435, 0.2616)):
        x, mean, std = [np.array(a, np.float32) for a in (x, mean, std)]
        x -= mean * 255
        x *= 1.0 / (255 * std)
        return x

    def denormalize(self, x, mean=(0.4914, 0.4822, 0.4465), std=(0.2471, 0.2435, 0.2616)):
        x, mean, std = [np.array(a, np.float32) for a in (x, mean, std)]
        x = x * (255 * std)
        x += mean * 255
        return x

    def __getitem__(self, index):
        train_path = self.trainsetFile[index]
        img1 = train_path
        img1 = Image.fromarray(img1.astype(np.uint8))
        img1 = np.array(img1).astype('float32')
        img1 = self.normalise(img1)
        img1 = img1.transpose((2, 0, 1))
        img1 = torch.from_numpy(img1)
        return img1
    def __len__(self):
        return len(self.trainsetFile)

