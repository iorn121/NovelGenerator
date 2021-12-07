import os
import codecs
import io
import chardet
from janome.tokenizer import Tokenizer
import markovify


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
        "'": "’",
    })
    text = text.translate(table)
    # print(text)
    t = Tokenizer()
    result = t.tokenize(text, wakati=True)
    result = list(result)
    splitted_text = ""
    for i in range(len(result)):
        splitted_text += result[i]
        if result[i] == "。" or result[i] == "！" or result[i] == "？":
            splitted_text += "\n"
        else:
            splitted_text += "　"
    return splitted_text


# データの保管先
ROOT_PATH_RAW = "/root/data/raw"
ROOT_PATH_UTF = "/root/data/utf"


def convert_charcode(raw_path, utf_path):
    """[RAWのテキストファイルからUTF-8形式にエンコードして返す]

    Args:
        raw_path ([string]): [description]
        utf_path ([string]): [description]

    Returns:
        [type]: [description]
    """
    splitted_text = ""
    raw_files = os.listdir(raw_path)
    utf_files = os.listdir(utf_path)
    for file in raw_files:
        file_path = raw_path + file
        with open(file_path, mode="rb") as f:
            chardet.detect()
            text = f.read()
        # fileだったら処理
        splitted_text += text_cleansing(text)+"\n"
    return splitted_text


splitted_text = recursive_file_check(ROOT_PATH)
sentence = None
while sentence == None:
    # モデルを生成
    text_model = markovify.NewlineText(splitted_text, state_size=2)
    # モデルから文章を生成
    sentence = text_model.make_sentence(tries=100, min_words=100)

with open("../output/markov_sentence.txt", mode="a") as f:
    f.write(sentence.replace(" ", ""))
    f.write("\n\n")
