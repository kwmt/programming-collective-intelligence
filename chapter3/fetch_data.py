import requests
import feedparser

def fetch_urls_data():
    d = feedparser.parse('https://note.com/recommend/rss')
    links = []

    for e in d.entries:
        if ('/n/' in e.link):
            s = e.link.split('/n/')
            links.append(f"{s[0]}/rss")

    return '\n'.join(links)

# サンプル
# result = getwordcounts('https://note.com/koukichi_t/rss')
# print(fetch_urls_data())


# noteのトップ記事からuser nameリスト取得する
def getUserNameList(page):
    print(f"{page}ページ取得中...")

    payload = {'page' : page}
    result = requests.get("https://note.com/api/v1/top_articles", params=payload)

    json = result.json()

    data = json['data']
    lastPage = data['last_page']
    nextPage = data['next_page']
    articles = data['articles']


    for article in articles:
        userNameList.append(article['user']['urlname'])

    if (lastPage):
        return
    else: 
        getUserNameList(nextPage)



userNameList = []

initial_page = 1
getUserNameList(initial_page)

urls = [f"https://note.com/{user}/rss" for user in userNameList]
    

print('\n'.join(urls))

