## 公式サンプル
https://resources.oreilly.com/examples/9780596529321/

## Python3系環境を構築する
```
$ git clone programming-collective-intelligence
$ cd programming-collective-intelligence
```
- activate
```
$ source programming-collective-intelligence/bin/activate
```

- deactivate
```
$ deactivate
```

## 似ているユーザーを探し出す

- 人々がどの程度似ているかを決める方法が必要
  - すべての人と比較して、`類似性スコア`を算出するとよい

- `類似性スコア`を算出する方法
  - いくつかあるが、ここでは`ユークリッド距離` と `ピアソン相関`について説明する

### ユークリッド距離によるスコア算出

- 人々が評価したアイテムを軸にとってグラフ上に人々を配置する。
- それぞれがどのくらい近いか見ることができる

ピタゴラスの定理によって距離を求めることができる。この距離が小さいほど似ているということになる。

```
>>> from math import sqrt
>>> sqrt(pow(5-4,2)+pow(4-1,2))
3.1622776601683795
```
しかし、似ていれば似ているほど高い数値を返す関数が必要。これを実現するには、１を加えて逆数を取れば良い（1を加えるのは、０除算エラーを防ぐため）。

```
>>> 1/(1+sqrt(pow(5-4,2)+pow(4-1,2)))
0.2402530733520421
```

この数式は、常に0から1の間の値を返す。値が1ならば、完全一致。

sim_distance関数をを実装

```
>>> from recommendations import sim_distance, critics
>>> sim_distance(critics, 'Lisa Rose', 'Gene Seymour')
0.14814814814814814
```

### ピアソン相関によるスコア算出

- 類似度を決めるもう少し洗練された手法として、ピアソン相関係数を用いる方法がある
- この相関係数は、2つのデータセットがある直線にどの程度沿っているかを示す。
- データが正規化されてないような状況では、ユークリッド距離より、良い結果を得られることが多い。

正規化されていない例としては、映画の評価が平均より厳しい場合など（AさんはBさんより甘く点数を付けている場合などは、ユークリッド距離によるスコアでは、たとえ好みが似ていたとしても、似ていないとみなされてしまう）。このような挙動を問題ないとみなすかは、作るアプリケーション次第。


- スコア算出手順
  - 両方の評者が得点を付けているアイテムのリストを取得する
  - それぞれの評者の評点の合計と、評点の平方の合計を算出
  - 評価をかけ合わせた値の合計を算出
  - ピアソン相関係数を算出


## アイテムを推薦する

似た評者を探し出すのはよいが、他の人が悪い評価しているにも関わらず、その似た評者が良いと評価している場合もありえる。

このような問題を解決するために、評者に順位付けをした重み付きスコアを算出することで、アイテムにスコアを付ける必要がある。

`getRecommendations`関数を参照

## 似ている製品

製品同士、似ているものを知りたい場合の話。

- 類似度を決めるためには、
  - 特定のアイテムを誰が好きなのか調べ、
  - 彼らが好きな他のアイテムを探す。

これは本質的には、先程行った人々の間の類似度を決めるやり方と同じで、人々とアイテムを入れ替えるだけで実現できる。つまりたとえば、

```
{'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5}, 
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5}}
```

を

```
{'Lady in the Water': {'Lisa Rose': 2.5, 'Gene Seymour': 3.5}, 
'Snakes on a Plane': {'Lisa Rose': 3.0, 'Gene Seymour': 3.5}}
```

このように変換すればよい。

変換関数は`transformPrefs`で、変換後に`topMatches`で、ある製品に似たものを取得することができる。

```
>>> from recommendations import critics, topMatches, transformPrefs
>>> movies=transformPrefs(critics)
>>> topMatches(movies, 'Superman Returns')
[(0.6579516949597695, 'You, Me and Dupree'), (0.4879500364742689, 'Lady in the Water'), (0.11180339887498941, 'Snakes on a Plane'), (-0.1798471947990544, 'The Night Listener'), (-0.42289003161103106, 'Just My Luck')]
```

マイナスの相関スコアは、この例では、'Superman Returns'を好む人は、Just My Luck'を好まない傾向にあるということを意味している。

さらに映画の評者を推薦してもらうこともできる。

```
>> getRecommendations(movies, 'Just My Luck')
[(4.0, 'Michael Phillips'), (3.0, 'Jack Matthews')]
```

## アイテムベースの強調フィルタリング

- これまでの使用技術は、ユーザーベースの強調フィルタリングと呼ばれている。
- これに変わるものとして、アイテムベースの協調フィルタリングという物がある
- 巨大なデータセットの場合は、アイテムベースの方は良い結果を生み出してくれる。
- アイテムベースの手順を簡単に
  - それぞれのアイテムに似ているアイテムたちを事前に計算しておく
  - そして、あるユーザーに推薦したくなったときに、そのユーザーが高く評価しているアイテムたちを参照し、それらに対して日得る順に重み付けされたアイテムたちのリストを作る。
  - アイテム間の関係は、人間同士の関係ほど頻繁に変わらないという点が重要。
    - それぞれのアイテムに似ているアイテムを見つけるために計算をし続ける必要はない

### アイテム間の類似度のデータセットを作る

### 推薦を行う

アイテムの類似性データセットは予め計算されているため、他の評価者たち類似性スコアを計算する必要がない点に注目。

## MovieLensのデータセットを使う

movielensの生データからデータセットを作成

```
>> prefs=loadMovieLens()
>>> prefs['87']
{'Naked Gun 33 1/3: The Final Insult (1994)': 4.0, 'Con Air (1997)': 4.0, 'Sabrina (1995)': 4.0, 'Waterworld (1995)': 4.0, 'To Wong Foo, Thanks for Everything! Julie Newmar (1995)': 3.0, 'Clueless (1995)': 4.0, 'Jurassic Park (1993)': 5.0, 'Brady Bunch Movie, The (1995)': 2.0, 'Son in Law (1993)': 4.0, 'Indiana Jones and the Last Crusade (1989)': 5.0, 'Good, The Bad and The Ugly, The (1966)': 5.0, 'Dead Poets Society (1989)': 5.0, 'Dead M
```

ユーザーベースの推薦は少し時間がかかる

```
>> getRecommendations(prefs, '87')[0:30]
[(5.0, 'They Made Me a Criminal (1939)'), (5.0, 'Star Kid (1997)'), (5.0, 'Santa with Muscles (1996)'), (5.0, 'Saint of Fort Washington, The (1993)'), (5.0, 'Marlene Dietrich: Shadow and Light (1996) '), (5.0, 'Great Day in Harlem, A (1994)'), (5
```

アイテムベースだと、最初の計算に時間かかるが、作ってしまえば、推薦は一瞬。ユーザーが増えても推薦にかかる時間は増えない。

```
>>> itemsim=calculateSimilarItems(prefs, n=50)
100 / 1664
200 / 1664
600 / 1664
>>> getRecommendedItems(prefs, itemsim, '87')[0:30]
[(5.0, "What's Eating Gilbert Grape (1993)"), (5.0, 'Vertigo (1958)'), (5.0, 'Usual Suspects, The (1995)'), (5.0, 'Toy Story (1995)'), (5.0, 'Titanic (1997)'), (5.0, 'Sword in the Stone, The (1963)'), (5.0, 'Stand by Me (1986)'), (
```

## ユーザーベース vs アイテムベース

- 疎なデータセットの場合、アイテムベースのフィルタリングの方が一般的にユーザーベースより性能がいい。
- 密なデータセットの場合は、大体同等の性能