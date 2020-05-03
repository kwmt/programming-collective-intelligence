import csv
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

readfile('blogdata.csv')