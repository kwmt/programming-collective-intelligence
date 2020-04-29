# 映画の評者といくつかの映画に対する彼らの評点のディクショナリ
critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
 'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5, 
 'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 
 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0, 
 'You, Me and Dupree': 3.5}, 
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
 'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
 'The Night Listener': 4.5, 'Superman Returns': 4.0, 
 'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 
 'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
 'You, Me and Dupree': 2.0}, 
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
 'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}


from math import sqrt

# person1とperson2の距離から類似性スコアを返す
def sim_distance(prefs, person1, person2):
    # 二人共評価しているアイテムのリストを取得
    shared_items={}
    for item in prefs[person1]:
        if item in prefs[person2]:
            shared_items[item] = 1

    if len(shared_items)==0: return 0

    # sum_of_squares = sum([pow(critics[person1][item]- critics[person2][item], 2) for item in critics[person1] if item in critics[person2]])
    sum_of_squares = sum(pow(prefs[person1][item]-prefs[person2][item], 2) for item in shared_items)

    return 1/(1+sum_of_squares)

def sim_pearson(prefs, p1, p2):
    # 二人共評価しているアイテムのリストを取得
    shared_items={}
    for item in prefs[p1]:
        if item in prefs[p2]:
            shared_items[item] = 1

    n = len(shared_items)
    if n==0: return 0

    # それぞれの評者の評点の合計を算出
    sum1 = sum([prefs[p1][item] for item in shared_items])
    sum2 = sum([prefs[p2][item] for item in shared_items])
    # それぞれの評者の評点の平方の合計を算出
    sum1Sqrt = sum([pow(prefs[p1][item], 2) for item in shared_items])
    sum2Sqrt = sum([pow(prefs[p2][item], 2) for item in shared_items])

    # 評価をかけ合わせた値の合計を算出
    pSum = sum([prefs[p1][item] * prefs[p2][item] for item in shared_items])

    # ピアソンによるスコアを計算
    num = pSum - (sum1*sum2) / n
    den = sqrt((sum1Sqrt - pow(sum1, 2) / n) * (sum2Sqrt - pow(sum2, 2) / n))
    if den == 0: return 0

    r = num / den
    return r