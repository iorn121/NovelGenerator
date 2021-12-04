# https://atmarkit.itmedia.co.jp/ait/articles/2103/19/news035.html

import os
import markov_generator

ROOT_PATH = "/root/data/"


def make_dic(splitted_text):
    word2id = {}
    id2word = {}
    for line in splitted_text:
        if line == '':  # 空行はスキップ
            continue
        if '（' in line or '―' in line:  # かっこと「―」を含む文はスキップ
            continue
        for word in line.split(' '):
            if word not in word2id:
                id = len(word2id) + 1  # id=0はパディング用にとっておく
                word2id[word] = id
                id2word[id] = word
    return word2id, id2word


splitted_text = markov_generator.recursive_file_check(ROOT_PATH)
