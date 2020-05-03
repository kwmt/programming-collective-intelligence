import csv
from math import sqrt

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

class biclsuster:
    def __init__(self, vec, left=None, right=None, distance=0.0, id=None):
        self.left = left
        self.right = right
        self.vec = vec
        self.id = id
        self.distance = distance