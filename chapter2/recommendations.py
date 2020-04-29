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
