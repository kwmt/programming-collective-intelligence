import feedparser
import re
import splitter

def getwordcounts(url):
    d = feedparser.parse(url)
    word_count = {}

    for e in d.entries:
        if 'summary' in e: summary=e.summary
        else: summary=e.description

        # 単語のリストを抽出
        words = getwords(e.title + ' ' + summary)
        for word in words:
            word_count.setdefault(word, 0)
            word_count[word] +=  1

    return d.feed.title, word_count

def getwords(html):
    txt = re.compile(r'<[->]+>').sub('', html)
    return [word.lower() for word in splitter.split(txt) if word != '']


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