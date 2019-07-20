import pandas as pd
import numpy as np
from graphviz import Digraph

# # データをロード
csv_path = r"data/data2.csv"
df = pd.read_csv(csv_path, encoding="shift-jis")

# # graphvizのAPIを使用してdot言語のスクリプト作成------------
# ## インスタンスを作成
dot = Digraph(comment="tree")
dot.format = "svg"  # 保存するフォーマット
# ## フォント設定
# PNG出力の際に日本語を表示するために必要
dot.attr('node', fontname="Meiryo UI")
# ## グラフ設定
dot.attr(rankdir="LR")  # グラフを横方向に設定
dot.attr("node", shape="box", width="1", color="black")  # ノードのスタイル

# ## ノード、エッジを作成
# ### 第1階層------------
# 第1階層を一意に変更
root_set = df.iloc[:, 0].drop_duplicates()
for i in range(len(root_set)):
    # ルートを1つ抽出
    root = root_set.iloc[i]
    # ルートの子となる行を抜き出し
    df_sub1 = df[df.iloc[:, 0]==root]
    # 人口を計算
    population_of_root = df_sub1.iloc[:, -1].sum()
    # ルートノードを作成
    dot.node("A{}".format(i), "{}\n({:,}人)".format(root, population_of_root))  # ルートの識別用にA1, A2などの名前を付ける
    # ### 第2階層------------
    # 第2階層を一意に変更
    node1_set = df_sub1.iloc[:, 1].drop_duplicates()
    for j in range(len(node1_set)):
        # 第2階層のノードを1つ抽出
        node1 = node1_set.iloc[j]
        # ルートの子となる行を抜き出し
        df_sub2 = df_sub1[df_sub1.iloc[:, 1]==node1]
        # 人口を計算
        population_of_node1 = df_sub2.iloc[:, -1].sum()
        # ノードを作成
        dot.node("B{}-{}".format(i, j), "{}\n({:,}人)".format(node1, population_of_node1))  # ルートの識別用にB1-1, B1-2などの名前を付ける
        # エッジを作成
        dot.edge("A{}".format(i), "B{}-{}".format(i, j))  # 第1階層と第2階層をつなぐ
        # ### 第3階層（最終階層）------------
        for k in range(len(df_sub2)):
            leaf = df_sub2.iloc[k, 2]
            # 人口を計算
            population_of_leaf = df_sub2.iloc[k, -1]
            # ノードを作成
            dot.node("C{}-{}-{}".format(i, j, k), "{}\n({:,}人)".format(leaf, population_of_leaf))

            # エッジを作成
            dot.edge("B{}-{}".format(i, j), "C{}-{}-{}".format(i, j, k))  # 第2階層と第3階層をつなぐ

# # 保存と表示
dot.render("output/tree_02.gv", view=True)

# （参考）
print(dot.source)  # dot言語での記述を表示
