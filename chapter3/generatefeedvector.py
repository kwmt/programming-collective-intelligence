import feedparser
import re

def getwordcounts(url):
    d = feedparser.parse(url)
    word_count = {}

    for e in d.entries:
        if 'summary' in e: summary=e.summary
        else: summary=e.description

        
    return summary

result = getwordcounts('https://note.com/koukichi_t/rss')
print(result)