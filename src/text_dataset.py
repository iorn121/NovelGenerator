import os
import torch
import sys
import io
import torch
import psutil
from memory_profiler import profile
import csv
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import matplotlib.pyplot as plt
import numpy as np
from corpus import make_dic, word2id
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


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


class Net(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_size,
                 batch_size=25, num_layers=1):
        super().__init__()
        self.hidden_size = hidden_size
        self.batch_size = batch_size
        self.num_layers = num_layers
        self.device = torch.device(
            'cuda:0' if torch.cuda.is_available() else 'cpu')

        self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=0)
        self.rnn = nn.RNN(embedding_dim, hidden_size,
                          batch_first=True, num_layers=self.num_layers)
        self.fc = nn.Linear(hidden_size, vocab_size)
        self = self.to(self.device)

    def init_hidden(self, batch_size=None):
        if not batch_size:
            batch_size = self.batch_size
        self.hidden_state = torch.zeros(self.num_layers, batch_size,
                                        self.hidden_size).to(self.device)

    def forward(self, x):
        x = self.embedding(x)
        x, self.hidden_state = self.rnn(x, self.hidden_state)
        x = self.fc(x)
        return x


@profile()
def train(model, dataloader, criterion, optimizer, epochs, vocab_size):
    device = model.device
    model.train()
    losses = []

    for epoch in range(epochs):
        running_loss = 0
        for cnt, (X_train, y_train) in enumerate(dataloader):
            optimizer.zero_grad()
            X_train, y_train = X_train.to(device), y_train.to(device)
            model.init_hidden()
            outputs = model(X_train)
            outputs = outputs.reshape(-1, vocab_size)
            y_train = y_train.reshape(-1)
            loss = criterion(outputs, y_train)
            running_loss += loss
            loss.backward()
            optimizer.step()
        losses.append(running_loss / cnt)

        print('+', end='')
        if epoch % 50 == 0:
            print(f'\nepoch: {epoch:3}, loss: {loss:.3f}')

    print(f'\nepoch: {epoch:3}, loss: {loss:.3f}')
    return losses


def main():
    author = 'person74'
    # word2idを呼び出してw2iに格納
    id_data = []
    print('will read')
    with open(f"../output/corpus/id_data_{author}.txt", mode="r", encoding="utf_8") as f:
        raw_text = f.read()
        for line in raw_text.split("\n"):
            if line == '':
                continue
            id_data.append(list(map(int, line.split(" "))))
    w2i = {}
    with open(f"../output/corpus/word2id_{author}.csv", mode="r", encoding="utf_8") as f:
        raw_csv = csv.reader(f)
        for line in raw_csv:
            w2i[line[0]] = int(line[1])

    print('read')

    dataset = TextDataset(id_data)
    BATCH_SIZE = 25
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE,
                            shuffle=True, drop_last=True)
    # iterator = iter(dataloader)
    # X_train, y_train = next(iterator)

    # vocab_size = len(w2i)+1
    # embedding_dimension = 5

    # embedding = nn.Embedding(vocab_size, embedding_dimension, padding_idx=0)
    # x = embedding(X_train)

    # hidden_size = 100
    # num_of_layers = 1
    # rnn = nn.RNN(input_size=embedding_dimension, hidden_size=hidden_size,
    #              batch_first=True, num_layers=num_of_layers)
    # h = torch.zeros(num_of_layers, batch_size, hidden_size)
    # r, h = rnn(x, h)
    # fc = nn.Linear(hidden_size, vocab_size)
    # o = fc(r)
    # o = o.reshape(-1, o.shape[-1])  # 2次元化
    # y_train = y_train.reshape(-1)  # 1次元化
    # c = nn.CrossEntropyLoss(ignore_index=0)
    # l = c(o, y_train)  # loss
    # Netインスタンス作成
    EMBEDDING_DIM = 300
    HIDDEN_SIZE = 300
    NUM_LAYERS = 1
    VOCAB_SIZE = len(w2i) + 1
    model = Net(VOCAB_SIZE, EMBEDDING_DIM, HIDDEN_SIZE, BATCH_SIZE, NUM_LAYERS)
    criterion = nn.CrossEntropyLoss(ignore_index=0)
    optimizer = torch.optim.SGD(model.parameters(), lr=0.03)

    epochs = 1
    losses = train(model, dataloader, criterion, optimizer, epochs, VOCAB_SIZE)
    plt.plot(losses)


if __name__ == "__main__":
    main()
