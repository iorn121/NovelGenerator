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
        self.x = [line[0:-1] for line in id_data]
        self.y = [line[1:] for line in id_data]

    def __len__(self):
        return self.data_length

    def __getitem__(self, idx):
        return torch.tensor(self.x[idx]), torch.tensor(self.y[idx])


def main():
    author = 'person74'
    text = []
    with open(f"../output/corpus/id_data_{author}.txt", mode="r", encoding="utf_8") as f:
        raw_text = f.read()
        for line in raw_text.split("\n"):
            if line == "":
                continue
            text.append(list(map(int, line.split(" "))))
    dataset = TextDataset(text)
    BS = 2
    dl = DataLoader(dataset, batch_size=BS, shuffle=True, drop_last=True)
    iterator = iter(dl)
    X_train, y_train = next(iterator)


if __name__ == "__main__":
    main()
