####################################################
#追加課題14-4：出力されたCSVファイルの可視化
#             温度異常検知で出力されたCSVファイルをグラフ化します。
####################################################
import pandas as pd                                 #データ分析ライブラリの読込み（pdで使えるようにしています。）
import matplotlib.pyplot as plt                     #グラフ作成ライブラリの読込み（pltで使えるようにしています。）

df = pd.read_csv("temperature_log.csv")             #csv読込み、dfという表形式データに格納

high = df[df["status"] == "HIGH"]                   #"status"列が"HIGH"だけのデータを抽出
low = df[df["status"] == "LOW"]                     #"status"列が"LOW"だけのデータを抽出

# plt.figure(figsize=(10,5))                          #グラフ作成（横幅10、縦幅5）

# plt.scatter(                                        #HIGHの散布図を描きます
#     high["timestamp"],                              #横軸を時間
#     high["temperature"],                            #縦軸を温度
#     color="red",                                    #赤色表示
#     label="HIGH"                                    #ラベル
# )

# plt.scatter(                                        #LOWの散布図を描きます
#     low["timestamp"],                               #横軸を時間
#     low["temperature"],                             #縦軸を温度
#     color="blue",                                   #青色表示
#     label="LOW"                                     #ラベル
# )

#折れ線グラフに変更
plt.figure(figsize=(12,6))

plt.plot(
    df["temperature"],
    marker="o"
)

plt.axhline(
    y=30,
    color="red",
    linestyle="--",
    label="High Limit"
)

plt.axhline(
    y=10,
    color="blue",
    linestyle="--",
    label="Low Limit"
)


plt.legend()                                        #凡例表示(可読性を考慮して)
# plt.xticks(rotation=45)                             #X軸の文字を回転(可読性を考慮して)
plt.grid()
plt.show()                                          #作成したグラフを画面に表示

print("temperature_graph.png を保存しました")