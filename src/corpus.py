# https://atmarkit.itmedia.co.jp/ait/articles/2103/19/news035.html

import os
import io
import sys
import csv
from janome.tokenizer import Tokenizer
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def text_cleansing(text):
    """[テキストの不要な文字を排除して、分かち書きに変換する]

    Args:
        text ([string]): [UTF-8にエンコードされた加工対象のテキスト]

    Returns:
        [string]: [綺麗にして分かち書きにしたテキスト]]
    """
    # 改行、スペース、問題を起こす文字の置換
    table = str.maketrans({
        '。': '.',
        '\n': '',
        '\r': '',
        '…': '',
        '、': '',
        '々': '',
        '「': '',
        '」': '.',
        '(': '（',
        ')': '）',
        '[': '［',
        ']': '］',
        '"': '”',
        "'": '’',
        '!': '！',
        '?': '？'
    })
    text = text.translate(table)
    t = Tokenizer()
    result = t.tokenize(text, wakati=True)
    result = list(result)
    splitted_text = ""
    for i in range(len(result)):
        splitted_text += result[i]
        if result[i] == "." or result[i] == "！" or result[i] == "？":
            splitted_text += "\n"
        else:
            splitted_text += " "
    return splitted_text


def convert_src_folder(src_path, dest_path):
    """[srcフォルダ内のテキストファイルをutf-8形式にして、別フォルダにコピー及び変換して追加する]

    Args:
        src_path ([string]): [shift-jis形式のテキストファイルを格納したフォルダ]
        dest_path ([string]): [utf-8形式のテキストファイルを格納するフォルダ]

    Returns:
        [list(string)]: [変換したファイルリストを返す]
    """
    src_files = os.listdir(src_path)
    dest_files = os.listdir(dest_path)

    for file_name in src_files:
        if file_name in dest_files:
            continue
        src_file_path = src_path + file_name
        dest_file_path = dest_path + file_name
        # ファイルオブジェクトをそれぞれ開く
        try:
            with open(src_file_path, mode="r", encoding="shift_jis") as src, open(dest_file_path, mode="w", encoding="utf_8") as dest:
                dest.write(src.read())
        except:
            return False
    return True


def make_dic(splitted_text):
    word2id = {}
    id2word = {}
    for line in splitted_text:
        if line == "":
            continue
        for word in line.split(' '):
            if word not in word2id:
                id = len(word2id) + 1  # id=0はパディング用にとっておく
                word2id[word] = id
                id2word[id] = word
    with open("../output/corpus_w2i.csv", mode="w", encoding="utf_8") as f:
        writer = csv.writer(f)
        for k, v in word2id.items():
            writer.writerow([k, v])
    with open("../output/corpus_i2w.csv", mode="w", encoding="utf_8") as f:
        writer = csv.writer(f)
        for k, v in id2word.items():
            writer.writerow([k, v])
    return word2id, id2word


def word2id(corpus, word2id, max_length=None):
    result = []
    for line in corpus:
        if line == "":
            continue
        now = []
        for word in corpus.split(' '):
            if max_length and len(result) > max_length:
                break
            if word not in word2id:
                continue
            now.append(word2id[word])
        result.append(now)
    with open("../output/w2i_text.csv", mode="w", encoding="utf_8") as f:
        f.write("\n".join(map(str, result)))
    return result


def id2word(id_data, id_to_word):
    result = ""
    for id in id_data:
        result += id_to_word[id]+" "
    with open("../output/i2w_text.csv", mode="w", encoding="utf_8") as f:
        f.write(result)
    return result


def main():
    # データの保管先
    ROOT_PATH_SRC = "/root/data/src/"
    ROOT_PATH_DEST = "/root/data/dest/"
    splitted_text = ""

    if not convert_src_folder(ROOT_PATH_SRC, ROOT_PATH_DEST):
        exit()

    files = os.listdir(ROOT_PATH_DEST)
    for text_file in files:
        text_file_name = ROOT_PATH_DEST+text_file
        with open(text_file_name, "r", encoding="utf-8") as f:
            text = f.read()
            splitted_text += text_cleansing(text)
            splitted_text += "\n"
    w2i, i2w = make_dic(splitted_text)

    # with open("../output/corpus_wakati.txt", mode="a", encoding="utf_8") as f:
    #     f.write(splitted_text)
    w2i_text = word2id(splitted_text, w2i)
    print(w2i_text)
    # i2w_text = id2word(w2i_text, i2w)


main()
