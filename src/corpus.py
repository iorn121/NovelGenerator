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

    return word2id, id2word


def word2id(corpus, word2id, max_length=100):
    result = []
    for line in corpus:
        if line == "":
            continue
        now = [word2id[word] for word in line.split(' ')]
        if len(now) > max_length:
            continue
        now += [0]*(max_length-len(now))
        result.append(now)
    return result


def id2word(id_data, id2word):
    result = ""
    for line in id_data:
        result += "".join([id2word[id] for id in line if id != 0])+"\n"
    return result


def main():
    # データの保管先
    author = 'person74'
    text = []
    with open(f"../output/aozora_text/wakati_{author}.txt", mode="r", encoding="utf_8") as f:
        raw_text = f.read()
        text.extend(raw_text.split("\n"))

    # word2id, id2wordを作成し保存
    w2i, i2w = make_dic(text)
    # with open("../output/corpus/word2id_{author}.csv", mode="w", encoding="utf_8") as f:
    #     writer = csv.writer(f)
    #     for k, v in w2i.items():
    #         writer.writerow([k, v])
    # with open("../output/corpus/id2word_{author}.csv", mode="w", encoding="utf_8") as f:
    #     writer = csv.writer(f)
    #     for k, v in i2w.items():
    #         writer.writerow([k, v])
    id_data = word2id(text, w2i)
    word_data = id2word(id_data, i2w)
    with open(f"../output/corpus/id_data_{author}.txt", mode="w", encoding="utf_8") as f:
        for line in id_data:
            f.write(" ".join(map(str, line)))
            f.write("\n")
    with open(f"../output/corpus/word_data_{author}.txt", mode="w", encoding="utf_8") as f:
        f.write(word_data)
    print("completed")


if __name__ == "__main__":
    main()
