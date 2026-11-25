# 動作確認
# print("Hello Python")

# """
#     課題1:変数
#         入力した名前と経験年数を表示する

#     補足:
#         name: 名前
#         experience: 経験年数

# """
# name = input("名前を入力してください：")
# print("こんばんは", name, "さん")

# experience = input("経験年数を入力してください：")
# print("経験年数は", experience, "年です")

# """
#     課題2:変数
#         自身の情報を5項目表示する

#     補足:
#         name: 名前
#         age:年齢
#         gender：性別
#         nationality：国籍
#         experience: 経験年数

# """

# """
#     課題3:条件分岐
#        点数判定プログラムを作成する

#     補足:
#         80以上：A
#         60以上：B
#         60未満：C

# """
# score = int(input("点数を入力してください："))
# if score < 0 or score > 100:
#     print("0～100の範囲で入力してください")
# elif score >= 80:
#     print("Aランクです")
# elif score <= 60:
#     print("Cランクです")
# else: 
#     print("Bランクです")

# """
#     課題4:条件分岐
#        テスト結果判定プログラムを作成する

#     補足:
#         テスト合格：pass
#         テスト不合格：fail

# """
# test_cases = [
#     {"id": "TC001", "expected": 100, "actual": 100},
#     {"id": "TC002", "expected": 200, "actual": 199},
#     {"id": "TC003", "expected": 300, "actual": 301},
# ]

# for tc in test_cases:
#     if tc["expected"] == tc["actual"]:
#         result = "PASS"
#     else:
#         result = "FAIL"

#     print(f'{tc["id"]}: {result}')

# """
#     課題5:繰返し
#        1～10までを連続して表示するプログラムを作成する

#     補足:
#         1
#         2
#         3
#         …
#         10

# """
# for ID in range(1, 11):
#     print(ID)

# """
#     課題6:繰返し
#        テストケース番号を表示するプログラムを作成する

#     補足:
#         TC001
#         TC002
#         TC003
#         TC004
#         TC005

# """
# for num in range(1, 6):
#     print(f"TEST{num:03d}", )

# """
#     課題7:関数
#        合計値を返すプログラムを作成する

#     補足:
       
# """
# def total(numbers):
#     return sum(numbers)

# data = [100, 200, 300, 400]
# print("合計：", total(data))

# """
#     課題8:関数
#        合計値を返す関数を作成する

#     補足:
#         def add(a, b):
#         return a + b

# """

# """
#     課題9:関数
#        テスト結果を判定する関数を作成する

#     補足:
#         check_result("OK")

# """

# """
#     課題10:リスト
#        テストケースの一覧を作成する

#     補足:
#         機能試験
#         性能試験
#         高負荷試験

# """

# """
#     課題11:リスト
#        試験項目を追加する

#     補足:
#         append()

# """

# """
#     課題12:辞書
#        テストケース情報を管理する

#     補足:
#         test_case = {
#             "ID": "TC001",
#             "Name": "機能試験",
#             "Result": "OK"
#         }

# """

# """
#     課題13:辞書
#        テストケース情報を複数件管理する

#     補足:
#         test_cases = [
#             {...},
#             {...},
#             {...}
#         ]

# """

# """
#     Week1最終課題:テストケース管理ツール（簡易版）
#        テストケースを管理する

#     補足:
#        test_cases = [
#             {"ID": "TC001", "Name": "機能試験", "Result": "OK"},
#             {"ID": "TC002", "Name": "性能試験", "Result": "NG"},
#             {"ID": "TC003", "Name": "高負荷試験", "Result": "OK"}
#         ]

# """




#ファイル操作練習
import csv  #CSVモジュールの読込み

total = 0   #合計値を保存する変数を用意
with open("sales.csv", encoding="utf-8")as f:   #CSVファイルを開く
    reader = csv.DictReader(f)  #CSVを辞書形式で読込み

    for row in reader:
        quantity = int(row["数量"])
        price = int(row["単価"])
        amount = quantity*price
        total +=amount  #売上金額の加算
print(f"売上合計：{total}円")


#画像処理練習
from bing_image_downloader import downloader

keywords = [
    "industrial robot",
    "factory robot arm",
    "AGV robot",
    "manufacturing equipment"
]

for word in keywords:
    downloader.download(
        word,
        limit=100,
        output_dir="dataset",
        adult_filter_off=True
    )

print("収集完了")