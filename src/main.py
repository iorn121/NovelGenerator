import os
import corpus
import text_dataset
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import matplotlib.pyplot as plt
import numpy as np


def main():
    # データの保管先
    ROOT_PATH_SRC = "/root/data/src/"
    ROOT_PATH_DEST = "/root/data/dest/"
    splitted_text = ""

    if not corpus.convert_src_folder(ROOT_PATH_SRC, ROOT_PATH_DEST):
        exit()

    files = os.listdir(ROOT_PATH_DEST)
    for text_file in files:
        text_file_name = ROOT_PATH_DEST+text_file
        with open(text_file_name, "r", encoding="utf-8") as f:
            text = f.read()
            splitted_text += corpus.text_cleansing(text)
            splitted_text += "\n"
    w2i, i2w = corpus.make_dic(splitted_text)

    with open("../output/corpus_wakati.txt", mode="a", encoding="utf_8") as f:
        f.write(splitted_text)
    w2i_data = corpus.word2id(splitted_text, w2i)
    i2w_data = corpus.id2word(w2i_data, i2w)
    dataset = text_dataset.TextDataset(w2i_data)
    print(len(dataset))
    # BS = 2
    # dl = DataLoader(dataset, batch_size=BS, shuffle=True, drop_last=True)
    # iterator = iter(dl)
    # X_train, y_train = next(iterator)
    # print(X_train.shape)
    # print(X_train)
    # print(y_train.shape)
    # print(y_train)


main()
