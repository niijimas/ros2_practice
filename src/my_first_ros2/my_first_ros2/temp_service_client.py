import rclpy                                        #ROS2の機能をPythonから使いための基本ライブラリ
from rclpy.node import Node                         #rclpy.nodeの中からROS2のノードを使うための設計図を読込む
from example_interfaces.srv import Trigger          #service通信で使われる標準のデータ型triggerを読込む（リクエストは空でレスポンスとして成功フラグと文字列を返す形式）

import csv                                          #CSVファイルを読み書きするためのライブラリ
from datetime import datetime                       #現在日時を取得するライブラリ
import os                                           #ファイルやフォルダを扱うライブラリ

# ####################################################
# #追加課題15：温度取得service
# #           serverを温度センサ役と仮定して、Clientからの要求（現在温度は？）に応答（25.3℃）して、Clientが温度を表示（現在温度：25.3℃）する。
# ####################################################
# class TempServiceClient(Node):                                      #ROS2の基本クラスである Node を継承して、TempServiceClientクラスを作成

#     def __init__(self):                                             #コンストラクタ
#         super().__init__('temp_service_client')                     #ROS2ネットワーク上に 'temp_service_client' という名前でこのノードを登録

#         self.client = self.create_client(                           #クライアントの作成
#             Trigger,                                                #データ型
#             'get_temperature'                                       #呼び出す際のサービス名
#         )

#         while not self.client.wait_for_service(timeout_sec=1.0):    #サーバーが起動しているか1.0秒間確認し、見つからなければ False を返す処理を繰り返すループ文
#             self.get_logger().info(                                 #秒待ってもサーバーが見つからなかった場合、ターミナルに「Waiting for Service...（サービス待機中...）」を表示（サーバーが起動するとループを抜けて次の処理に進む）
#                 'Waiting for Service...'
#             )

#     def send_request(self):                                         #実際にサーバーへ要求を送り、結果を受け取るためのメソッドを定義

#         request = Trigger.Request()                                 #rigger 型の「リクエスト（要求）用データ」をrequestに代入

#         future = self.client.call_async(request)                    #サーバーへリクエストを非同期（async）で送信（非同期＝返事の代わりに、「あとで結果が届く予約票（future オブジェクト）」を送信）

#         rclpy.spin_until_future_complete(                           #予約票（future）にサーバーからの返事が届くまで、このノード（self）を待機させて通信処理を回し続ける
#             self,
#             future
#         )

#         return future.result()                                      #futureに届いた実際の返信データ（response）を .result() で取り出し、呼び元に返却


# def main(args=None):                                                #main関数の定義

#     rclpy.init(args=args)                                           #ROS2通信システム全体の初期化

#     node = TempServiceClient()                                      #クライアントの呼び出し

#     response = node.send_request()                                  #send_request()の結果をresponseに代入

#     print(                                                          #response.messageのデータを表示する
#         f'現在温度：{response.message}℃'
#     )

#     node.destroy_node()                                             #終了処理
#     rclpy.shutdown()                                                


# if __name__ == '__main__':                                          #おまじない
#     main()

####################################################
#課題15-1：設備異常監視
#       　サーバーに設備の状態を問い合わせ、結果が False（異常）だった場合に警告メッセージを出すクライアントを作成する。
####################################################
class EquipmentMonitorClient(Node):

    def __init__(self):                                             #コンストラクタ
        super().__init__('equipment_monitor_client')                #ROS2ネットワーク上に 'equipment_monitor_client' という名前でこのノードを登録

        self.client = self.create_client(                           #クライアントを作成してself.clientに代入
            Trigger,                                                #データ型
            'check_equipment'                                       #サービス名
        )

        while not self.client.wait_for_service(timeout_sec=1.0):    #サーバーが起動するまで1秒おきに確認を繰り返すループ
            self.get_logger().info('監視サーバーの起動を待機中...')    #サーバーが応答しない場合、ターミナルに「監視サーバーの起動を待機中...」と表示

    def check_status(self):                                         #判定結果を受け取るためのメソッドを定義
        request = Trigger.Request()                                 #Trigger型のリクエスト用データを用意してrequest代入
        future = self.client.call_async(request)                    #サーバーへリクエストを非同期で送信
        rclpy.spin_until_future_complete(self, future)              #予約票（future）にサーバー結果が届くまで、クライアントノード（self）の通信処理を回しながら待機
        return future.result()                                      #futureに届いた実際の返信データ（response）を .result() で取り出し、呼び出し元へ返却
    
# #案1
# def save_alarm_log(message):                                      #ログを保存する関数定義
#     with open(                                                    #ファイルを開く命令（with ～ as f:を使うことで開く、書き込む、閉じるを自動で行う）
#         'equipment_alarm_log.csv',                                #ファイル名
#         'a',                                                      #ファイルを開くモード（a=既存データを消さずに末尾へ追加）
                                                                    #   r	読み込み
                                                                    #   w	新規作成して上書き
                                                                    #   a	追記
                                                                    #   x	新規作成のみ
#         newline='',                                               #余分な空行を避ける（CSVではお決まりの記載）
#         encoding='utf-8'                                          #文字コード
#     ) as f:

#         writer = csv.writer(f)                                    #CSVの書き込みオブジェクトを作成

#         writer.writerow([                                         #CSVの１行を書き込む命令
#             datetime.now().strftime('%Y-%m-%d %H:%M:%S'),         #現在時刻を取得して文字列に変換
#             'TEMPERATURE_HIGH',                                   #CSVに表示する異常の種類
#             message                                               #関数に渡された異常の内容
#         ])                                                        #リストの終了

#案2
def save_alarm_log(message):                                        #ログを保存する関数定義

    file_exists = os.path.isfile(                                   #equipment_alarm_log.csvファイルがあるか調べる
        'equipment_alarm_log.csv'                                   #
    )

    with open(                                                      #ファイルを開く
        'equipment_alarm_log.csv',                                  #ファイル名
        'a',                                                        #ファイルを開くモード
        newline='',                                                 #空行対策
        encoding='utf-8-sig'                                        #文字コード
    ) as f:                                                         #ファイルを閉じる

        writer = csv.writer(f)                                      #CSVの書き込みオブジェクト作成

        if not file_exists:                                         #CSVファイルが存在しない場合にヘッダを作成する
            writer.writerow([                                       
                "timestamp",                                        
                "status",                                           
                "message"                                           
            ])

        writer.writerow([                                           #CSVへの書き込み（1行ずつ）
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),           #現在時刻を取得して文字列に変換
            "ALARM",                                                #CSVにアラームと表示
            message                                                 #異常の内容を表示
        ])

def main(args=None):                                                #main関数を定義

    rclpy.init(args=args)                                           #ROS2の通信初期化

    node = EquipmentMonitorClient()                                 #クライアントの結果をnodeに格納

    response = node.check_status()                                  #サーバーからの結果をresponseに格納

    if response.success:                                            #response.successの中身を判定
        print(f'【OK】{response.message}')                          #Trueの場合、画面に'【OK】{response.message}'を表示
    else:
        print(f'【警告・停止推奨】{response.message}')                  #Falseの場合、画面に'【警告・停止推奨】{response.message}'を表示
        save_alarm_log(response.message)

    node.destroy_node()                                             #終了処理
    rclpy.shutdown()


if __name__ == '__main__':                                          #おまじない
    main()

