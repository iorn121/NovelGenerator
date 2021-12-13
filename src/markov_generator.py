import os
import corpus
import markovify


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
