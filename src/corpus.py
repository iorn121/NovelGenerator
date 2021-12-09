# https://atmarkit.itmedia.co.jp/ait/articles/2103/19/news035.html

import os
import csv
import markov_generator as mg


def make_dic(splitted_text):
    word2id = {}
    id2word = {}
    for word in splitted_text.split('　'):
        if word not in word2id:
            id = len(word2id) + 1  # id=0はパディング用にとっておく
            word2id[word] = id
            id2word[id] = word
    return word2id, id2word


def word2id(corpus, word2id, max_length):
    result = []
    for word in corpus.split('　'):
        if len(result) > max_length:
            break
        result.append(word2id[word])
    return result


def main():
    # データの保管先
    ROOT_PATH_SRC = "/root/data/src/"
    ROOT_PATH_DEST = "/root/data/dest/"
    splitted_text = ""

    if not mg.convert_src_folder(ROOT_PATH_SRC, ROOT_PATH_DEST):
        exit()

    files = os.listdir(ROOT_PATH_DEST)
    for text_file in files:
        text_file_name = ROOT_PATH_DEST+text_file
        with open(text_file_name, "r", encoding="utf-8") as f:
            text = f.read()
            splitted_text += mg.text_cleansing(text)
            splitted_text += "\n"
    w2i, i2w = make_dic(splitted_text)

    with open("../output/corpus_wakati.txt", mode="a") as f:
        f.write(splitted_text)
    with open("../output/corpus_w2i.csv", mode="w") as f:
        writer = csv.writer(f)
        for k, v in w2i.items():
            writer.writerow([k, v])
    with open("../output/corpus_i2w.csv", mode="w") as f:
        writer = csv.writer(f)
        for k, v in i2w.items():
            writer.writerow([k, v])
    w2i_text = word2id(splitted_text, w2i, 100)
    with open("../output/w2i_text.csv", mode="w") as f:
        f.write("\n".join(map(str, w2i_text)))


main()
