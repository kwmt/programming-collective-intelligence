import csv
from math import sqrt
from PIL import Image, ImageDraw, ImageFont

def readfile(filename):
    # タイトル(単語)
    colnames=[]
    # ブログタイトル
    rownames = []
    # 頻出度
    data = []

    with open(filename) as f:
        reader = csv.reader(f)
        l = [row for row in reader]
        colnames = l[0][1:]
        lines = [row for row in l[1:]]
        for line in lines:
            rownames.append(line[0])
            data.append([float(x) for x in line[1:]])
    
    return rownames, colnames, data

# ピアソン相関係数を求める
def pearson(v1, v2):
    # 単純な合計
    sum1 = sum(v1)
    sum2 = sum(v2)

    # 平方の合計
    sum1Sq = sum(pow(v, 2) for v in v1)
    sum2Sq = sum(pow(v, 2) for v in v2)

    # 積の合計
    pSum = sum([v1[i]*v2[i] for i in  range(len(v2))])

    # ピアソンによるスコアを算出
    num = pSum - (sum1 * sum2 / len(v2))
    den = sqrt((sum1Sq - pow(sum1, 2) / len(v1)) * (sum2Sq - pow(sum2, 2) / len(v2)))
    if (den == 0): return 0

    # ピアソン相関係数は２つのアイテムが完全に一致するときは1.0になり、逆は0.0に近くなる。
    # しかし今回はアイテム同士が似ていれば似ているほど小さい値を返したいので、1からピアソン相関係数を引いた数値を返している。
    return 1.0 - num / den

class bicluster:
    def __init__(self, vec, left=None, right=None, distance=0.0, id=None):
        self.left = left
        self.right = right
        self.vec = vec
        self.id = id
        self.distance = distance

def hcluster(rows, distance=pearson):
    distances={}
    currentclustid=-1

   
    # クラスタは最初は行たち
    clust = [bicluster(rows[i], id=i) for i in range(len(rows))]


    while(len(clust) > 1):
        lowestpair = (0, 1)
        closest = distance(clust[0].vec, clust[1].vec)
        

        # すべての組をループし、もっとも距離の近い組を探す
        for i in range(len(clust)):
            for j in range(i+1, len(clust)):
                # 距離をキャッシュして、あればそれを使う
                if (clust[i].id, clust[j].id) not in distances:
                    distances[(clust[i].id, clust[j].id)] = distance(clust[i].vec, clust[j].vec)
                
                d = distances[(clust[i].id, clust[j].id)]
                
                if d < closest:
                    closest = d
                    lowestpair = (i, j)
        
        # ２つのクラスタの平均を計算する
        mergevec = [(clust[lowestpair[0]].vec[i] + clust[lowestpair[1]].vec[i])/ 2.0 
            for i in range(len(clust[0].vec))]

        
        #　新たにクラスタを作成
        newcluster = bicluster(mergevec, left=clust[lowestpair[0]],
                        right=clust[lowestpair[1]],
                        distance=closest,id=currentclustid)
         # 元のセットではないクラスタのIDは負にする
        currentclustid = -1
        del clust[lowestpair[1]]
        del clust[lowestpair[0]]
        clust.append(newcluster)

    return clust[0]


def printclust(clust, labels=None, n=0):
    for i in range(n): print('\t'),
    if clust.id<0:
        print('-')

    else:
        if labels==None: print(clust.id)
        else: print(labels[clust.id])

    if clust.left != None: printclust(clust.left, labels=labels, n = n+1)
    if clust.right != None: printclust(clust.right, labels=labels, n = n+1)

def getheight(clust):
  # Is this an endpoint? Then the height is just 1
  if clust.left==None and clust.right==None: return 1

  # Otherwise the height is the same of the heights of
  # each branch
  return getheight(clust.left)+getheight(clust.right)

def getdepth(clust):
    if clust.left == None and clust.right == None: return 0
    return max(getdepth(clust.left), getdepth(clust.right)) + clust.distance


def drawdendrogram(clust,labels,jpeg='clusters.jpg'):
  # height and width
  h=getheight(clust)*20
  w=1200
  depth=getdepth(clust)

  # width is fixed, so scale distances accordingly
  scaling=float(w-150)/depth

  # Create a new image with a white background
  img=Image.new('RGB',(w,h),(255,255,255))
  draw=ImageDraw.Draw(img)

  draw.line((0,h/2,10,h/2),fill=(255,0,0))    

  # Draw the first node
  drawnode(draw,clust,10,(h/2),scaling,labels)
  img.save(jpeg,'JPEG')

def drawnode(draw,clust,x,y,scaling,labels):
  if clust.id<0:
    h1=getheight(clust.left)*20
    h2=getheight(clust.right)*20
    top=y-(h1+h2)/2
    bottom=y+(h1+h2)/2
    # Line length
    ll=clust.distance*scaling
    # Vertical line from this cluster to children    
    draw.line((x,top+h1/2,x,bottom-h2/2),fill=(255,0,0))    
    
    # Horizontal line to left item
    draw.line((x,top+h1/2,x+ll,top+h1/2),fill=(255,0,0))    

    # Horizontal line to right item
    draw.line((x,bottom-h2/2,x+ll,bottom-h2/2),fill=(255,0,0))        

    # Call the function to draw the left and right nodes    
    drawnode(draw,clust.left,x+ll,top+h1/2,scaling,labels)
    drawnode(draw,clust.right,x+ll,bottom-h2/2,scaling,labels)
  else:   
    # If this is an endpoint, draw the item label
    fnt = ImageFont.truetype('./Kokoro.otf',30) #ImageFontインスタンスを作る
    draw.text((x+5,y-7),labels[clust.id],(0,0,0), font=fnt)


blognames, words, data= readfile('blogdata.csv')
clust=hcluster(data)

drawdendrogram(clust, blognames, jpeg='blogclust.jpg')
