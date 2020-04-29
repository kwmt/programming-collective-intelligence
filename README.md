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