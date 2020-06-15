import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class clawler:
    # データベースの名前でクローラを初期化
    def __init__(self, dbname):
        pass

    def __del__(self):
        pass

    def dbcommit(self):
        pass

    def getentryid(self, table, field, value, createnew=True):
        return None

    def addtoindex(self, url, soup):
        print(f"Indexing {url}")

    def gettextonly(self, soup):
        return None
    
    def separatewords(self, test):
        return None
    
    def isindexed(self, url):
        return None
    
    def addlinkref(self, urlFrom, urlTo, linkText):
        pass

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
        pass



pagelist = ['https://kwmt27.net/']
crawler = clawler('')
crawler.crawl(pagelist)