import time
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


def scrape_all_writing_text(author: str):
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


def main():
    author = 'person74'
    data = scrape_all_writing_text(author)

    # 文章を書き出す
    with open(f"../output/aozora_text/text_{author}.txt", mode="w") as f:
        f.write('\n'.join(data))


if __name__ == '__main__':
    main()
