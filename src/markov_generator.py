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
    sentence = None
    while sentence == None:
        # モデルを生成
        text_model = markovify.NewlineText(splitted_text, state_size=2)
        # モデルから文章を生成
        sentence = text_model.make_sentence(tries=100, min_words=100)

    with open("../output/markov_sentence.txt", mode="a") as f:
        f.write(sentence.replace(" ", ""))
        f.write("\n\n")


main()
