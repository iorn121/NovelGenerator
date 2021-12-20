from janome.tokenizer import Tokenizer
import re
from urllib import request
from bs4 import BeautifulSoup
import io
import sys
import glob
import time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def scrape_text(url: str):
    """[青空文庫のURLから本文テキストをスクレイピングして整形する]

    Args:
        url (str): [青空文庫の本文が記載されたXML]

    Returns:
        [list(str)]: [本文のうち、改行部分で分割されたリスト]
    """

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


def scrape_all_writing_text(author: str):
    """[作者番号を入力したら作品全てをスクレイピングして、テキストを整形した後リストで返す]

    Args:
        author (str): [person+作者番号（梶井基次郎なら74）]

    Returns:
        [type]: [全作品の全本文のリスト]
    """

    # URLのドメインを定義して、作者番号でスクレイピング
    base_url = 'http://www.aozora.gr.jp/index_pages/'
    person = author+'.html'
    response = request.urlopen(base_url+person)
    soup = BeautifulSoup(response, features="html.parser")

    text_list = []

    url_list = [item['href'] for item in soup.find('ol').find_all('a')]
    for url in url_list:
        title_page_url = base_url+url
        title_page_response = request.urlopen(title_page_url)
        title_page_soup = BeautifulSoup(
            title_page_response, features="html.parser")
        html_path = title_page_soup.find_all('div', align='right')[
            1].find_all('a')[1]['href']
        title_page_url = re.sub('card\d+\.html', '', title_page_url)
        result = scrape_text(title_page_url + html_path)
        text_list.extend(result)
        time.sleep(5)

    return text_list


def make_wakati(text: str):
    t = Tokenizer()
    result = []
    for line in text:
        word = list(t.tokenize(line, wakati=True))
        result.append(word)
    return result


def main():
    author = 'person74'
    # data = scrape_all_writing_text(author)

    text = []
    # 文章を読み込む
    with open(f"../output/aozora_text/text_{author}.txt", mode="r", encoding="utf_8") as f:
        raw_text = f.read()
        text.extend(list(raw_text.split("\n")))
    result = make_wakati(text)
    with open(f"../output/aozora_text/wakati_{author}.txt", mode="w", encoding="utf_8") as f:
        for line in result:
            f.write(" ".join(line))
            f.write("\n")


if __name__ == '__main__':
    main()
