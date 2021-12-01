import os
from janome.tokenizer import Tokenizer
import markovify


def text_cleansing(text):
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


ROOT_PATH = "/root/data/"


def recursive_file_check(path):
    splitted_text = ""
    files = os.listdir(path)
    for file in files:
        file_path = path+file
        with open(file_path, mode="r", encoding="shift_jis") as f:
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
