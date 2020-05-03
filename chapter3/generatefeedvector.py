import feedparser
import re
import splitter
import csv

def getwordcounts(url):
    d = feedparser.parse(url)
    word_count = {}

    for e in d.entries:
        if 'summary' in e: summary=e.summary
        else: summary=e.description

        # 単語のリストを抽出
        html = f"{e.title} {summary}"
        # print("------html---------")
        # print(html)
        words = getwords(html)
        # print("------words---------")
        # print(words)
        for word in words:
            word_count.setdefault(word, 0)
            word_count[word] +=  1

    return d.feed.title, word_count

def getwords(html):
    txt = re.compile(r'<[^>]+>').sub('', html)
    # print("------txt---------")
    # print(txt)
    return [word.lower() for word in splitter.split(txt) if word != '']



def main():
    print("------main---------")
    # 各URLの単語を計測
    apcount = {}
    wordcounts={}
    feedlist = [line for line in open('feedlist.txt')]
    # [
    #     'https://note.com/mid_architecture/rss', 
    # # 'https://note.com/ynsmr/rss', 
    # 'https://note.com/harukamano/rss',
    # 'https://note.com/naffix/rss'
    # ] 
    

    for feedurl in feedlist:
        try:
            print(f"{feedurl} 解析中...")
            title, wc = getwordcounts(feedurl)
            wordcounts[title] = wc
            # print("------wordcounts---------")
            # print(wordcounts)
            for word, count in wc.items():
                apcount.setdefault(word,0)
                if count > 1:
                    apcount[word]+=1
            # print("------apcount---------")
            # print(apcount.items())
        except:
            print(f"Failed to parse feed {feedurl}")

    print('---filtering----------------------')

    # 単語の出現数リストを生成
    # 出現率が多すぎるもの、低すぎるものをフィルタリングする。（theのような単語はほとんどすべての存在するため）
    wordlist=[]
    for w, bc in apcount.items():
        frac = float(bc) / len(feedlist)
        if frac > 0.1 and frac < 0.5: wordlist.append(w)

    # ブログのリストを縦に、単語リストを横に表示し、各ブログの単語の出現数をあらわした表を作成
    with open('blogdata.csv', 'w') as f:
        writer = csv.writer(f)
        titles = ["Blog"]
        titles.extend(wordlist)
        writer.writerow(titles)
    
        for blog, wc in wordcounts.items():
            values=[blog]
            print(blog)
            for word in wordlist:
                if (word in wc): values.append(wc[word])
                else: values.append(0)
            writer.writerow(values)
