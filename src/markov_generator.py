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
    print(text)
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


with open("../data/bocchan.txt", mode="r", encoding="shift_jis") as f:
    text = f.read()

splitted_text = text_cleansing(text)
print(splitted_text)
