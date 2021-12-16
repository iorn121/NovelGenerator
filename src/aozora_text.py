from bs4 import BeautifulSoup
from urllib import request
import re


def scrape_text(url: str):
    # URLでスクレイピング
    response = request.urlopen(url)
    soup = BeautifulSoup(response, features="html.parser")
    response.close()

    # 本文要素のみ取得
    main_text = soup.find('div', class_='main_text')

    # ルビの読み仮名要素を削除し、本文をテキストに整形
    tags_to_delete = main_text.find_all(['rp', 'rt', 'h4'])
    for tag in tags_to_delete:
        tag.decompose()
    main_text = main_text.get_text()

    # 改行を全削除して、付け直し
    main_text = main_text.replace('\r', '').replace(
        '\n', '').replace('\u3000', '')
    main_text = main_text.replace('「', '').replace('」', '\n')
    main_text = re.sub('([！？。])', r'\1\n', main_text)
    main_text = main_text.replace('\n\n', '\n')
    text_list = main_text.splitlines()

    return text_list


def main():
    url = 'https://www.aozora.gr.jp/cards/000074/files/429_19794.html'
    text_list = scrape_text(url)

    # 文章を書き出す
    with open(f"../output/aozora_text/text_ShironoAruMachinite.txt", mode="w") as f:
        f.write('\n'.join(text_list))


if __name__ == '__main__':
    main()
