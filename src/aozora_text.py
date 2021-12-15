from bs4 import BeautifulSoup
from urllib import request

url = 'https://www.aozora.gr.jp/cards/000074/files/427_19793.html'
response = request.urlopen(url)
soup = BeautifulSoup(response)
response.close()
print(soup)
