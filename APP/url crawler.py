import requests
from bs4 import BeautifulSoup

url = "https://www.baidu.com"
html = requests.get(url)
html.encoding = 'utf-8'
soup = BeautifulSoup(html.text, "html.parser")
title = soup.find('title').text
# print(title)