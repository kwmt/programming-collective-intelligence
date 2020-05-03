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


# 各URLの単語を計測
apcount = {}
wordcounts={}
feedlist = [line for line in open('feedlist.txt')]

for feedurl in feedlist:
    try:
        title, wc = getwordcounts(feedurl)
        wordcounts[title] = wc
        for word, count in wc.items():
            apcount.setdefault(word,0)
            if count > 1:
                apcount[word]+=1
    except:
        print(f"Failed to parse feed {feedurl}")

# 単語の出現数リストを生成
# 出現率が多すぎるもの、低すぎるものをフィルタリングする。（theのような単語はほとんどすべての存在するため）
wordlist=[]
for w, bc in apcount.items():
    frac = float(bc) / len(feedlist)
    if frac > 0.1 and frac < 0.5: wordlist.append(w)

# ブログのリストを縦に、単語リストを横に表示し、各ブログの単語の出現数をあらわした表を作成
out = open('blogdata.txt', 'w')
out.write('Blog')
for word in wordlist: out.write(f"\t{word}")

for blog, wc in wordcounts.items():
    out.write(blog)
    for word in wordlist:
        if word in wc: out.write(f"\t{wc[word]}")
        else: out.write("\t0")
    out.write("\n")
