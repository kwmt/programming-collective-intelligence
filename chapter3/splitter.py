
import os
from urllib.request import urlopen
import urllib.parse
from bs4 import BeautifulSoup


# 形態要素解析した結果をリストで返す

# app_idは こちらのclient idを指定
# https://e.developer.yahoo.co.jp/dashboard/app.detail/IQfwfD6ypEMtT44-
# YAHOO_CLIENT_APP_ID=<app_id> python splitter.py という感じで実行する。
# https://developer.yahoo.co.jp/webapi/jlp/ma/v1/parse.html

appId = os.environ['YAHOO_CLIENT_APP_ID']
pageUrl = "https://jlp.yahooapis.jp/MAService/V1/parse"

def split(sentence, appid= appId, results= 'ma', filter='1|2|4|5|9|10'):
    sentence=urllib.parse.quote_plus(sentence.encode('utf-8'))
    query= f"{pageUrl}?appid={appid}&results={results}&uniq_filter={filter}&sentence={sentence}"
    result = urlopen(query)
    soup = BeautifulSoup(result, 'html.parser')

    try:
        return [l.surface.string for l in soup.ma_result.word_list]
    except: return[]
        

def fetch_urls():
    result = urlopen('https://note.com/')
    soup = BeautifulSoup(result, 'html.parser')

    links = [url.get('href') for url in soup.find_all('a')]
    print(links)

fetch_urls()