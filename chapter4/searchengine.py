import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sqlite3
import splitter

# Create a list of words to ignore
ignorewords={'the':1,'of':1,'to':1,'and':1,'a':1,'in':1,'is':1,'it':1}

class clawler:
    # データベースの名前でクローラを初期化
    def __init__(self, dbname):
        self.con = sqlite3.connect(dbname)

    def __del__(self):
        self.con.close()

    def dbcommit(self):
        self.con.commit()

    def getentryid(self, table, field, value, createnew=True):
        query = 'select rowid from %s where %s=' % (table, field)
        sql = query + '=?'
        data = (value,)
        cur = self.con.execute(sql, data)
        res = cur.fetchone()
        if res == None:
            q = 'insert into %s (%s) values' % (table, field)
            s = q + '(?)'
            cur = self.con.execute(s, (value,))
            return cur.lastrowid
        else:
            return res[0]

    def addtoindex(self, url, soup):
        if self.isindexed(url): return
        # print(f"Indexing {url}")

        # 個々の単語を取得する
        text = self.gettextonly(soup)
        words = self.separatewords(text)

        # URL idを取得する
        urlid = self.getentryid('urllist', 'url', url)

        print(f"addtoindex urlid: {urlid}")
        # それぞれの単語と、このurlのリンク
        for i in range(len(words)):
            word = words[i]
            if word in ignorewords: continue
            wordid = self.getentryid('wordlist', 'word', word)
            print(f"addtoindex:i: {i} worid: {wordid}")
            self.con.execute("insert into wordlocation(urlid, wordid, location)  \
                values (%d, %d, %d)" % (urlid, wordid, i))



    # ページ内の単語を探し出す
    def gettextonly(self, soup):
        v = soup.string
        if v == None:
            c = soup.contents
            resulttext = ''
            for t in c:
                subtext = self.gettextonly(t)
                resulttext += subtext + '\n'
            return resulttext
        else:
            return v.strip()
    
    def separatewords(self, text):
        # print(f"{text}")
        try:
            return [s.lower() for s in splitter.split(text) if s != '']
        except:
            print(f"separatewords{text}")
            return []
    
    def isindexed(self, url):
        u = self.con.execute('select rowid from urllist where url=?', (url, )).fetchone()
        if u != None:
            v = self.con.execute('select * from wordlocation where urlid=%d' % u[0]).fetchone()
            if v != None: return True
        else:
            return False
    
    def addlinkref(self, urlFrom, urlTo, linkText):
        words = self.separatewords(linkText)
        fromid = self.getentryid('urllist', 'url', urlFrom)
        toid = self.getentryid('urllist', 'url', urlTo)
        if fromid == toid: return

        cur = self.con.execute("insert into link(fromid, toid) values (%d, %d)" % (fromid, toid))
        linkid = cur.lastrowid
        for word in words:
            if word in ignorewords: continue
            wordid = self.getentryid('wordlist', 'word', word)
            self.con.execute("insert into linkwords(linkid, wordid) values (%d, %d)" % (linkid, wordid)) 


    def crawl(self, pages, depth=2):
        for i in range(depth):
            newpages=set()
            for page in pages:
                try:
                    c=requests.get(page)
                except:
                    print(f"Could not open {page}")
                    continue
                soup = BeautifulSoup(c.text, 'html.parser')
                self.addtoindex(page, soup)

                links = soup('a')
                for link in links:
                    if ('href' in dict(link.attrs)):
                        url = urljoin(page, link['href'])
                        if (url.find("'") != -1): continue
                        url=url.split('#')[0] # アンカーを取り除く
                        if ((url[0:4] == 'http' or url[0:4] == 'https') and not self.isindexed(url)):
                            newpages.add(url)
                        linkText = self.gettextonly(link)
                        self.addlinkref(page, url, linkText)
            
                self.dbcommit()
            pages = newpages



    def createindextables(self):
        self.con.execute('create table urllist(url)')
        self.con.execute('create table wordlist(word)')
        self.con.execute('create table wordlocation(urlid, wordid, location)')
        self.con.execute('create table link(fromid integer, toid integer)')
        self.con.execute('create table linkwords(wordid, linkid)')
        self.con.execute('create index wordidx on wordlist(word)')
        self.con.execute('create index urlidx on urllist(url)')
        self.con.execute('create index wordurlidx on wordlocation(wordid)')
        self.con.execute('create index urltoidx on link(toid)')
        self.con.execute('create index urlfromidx on link(fromid)')
        self.dbcommit()



pagelist = ['https://kwmt27.net/']
crawler = clawler('searchindex.db')
# crawler.createindextables()
crawler.crawl(pagelist)

# [row for row in crawler.con.execute('select rowid from wordlocation where wordid=1')]