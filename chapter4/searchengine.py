
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
        pass

    def createindextables(self):
        pass