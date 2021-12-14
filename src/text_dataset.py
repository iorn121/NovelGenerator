import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import matplotlib.pyplot as plt
import numpy as np


class TextDataset(Dataset):
    def __init__(self, id_data):
        super().__init__()
        self.data_length = len(id_data)
        self.x = id_data[0:-1]
        self.y = id_data[1:]

    def __len__(self):
        return self.data_length

    def __getitem__(self, idx):
        return torch.tensor(self.x[idx]), torch.tensor(self.y[idx])
