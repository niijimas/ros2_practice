import rclpy                        #ROS2のPythonライブラリ（rclpy.spin(node)等の使用にするために必要です。）
from rclpy.node import Node         #ROS2ノードを使うためのクラスを読込む（ROS2の「Node」を作るために必要です。）
from std_msgs.msg import Float32    #メッセージ型を読込む（Float32＝小数点付き数値）
import time                         #時刻や待ち時間を扱うための標準ライブラリ
import csv                          #CSVファイルの読み書きを行うための標準ライブラリ
from datetime import datetime       #日時を扱うためのライブラリ


# ####################################################
# #課題13：1秒おきに温度を受信するSubscriber
# ####################################################
# class TempSubscriber(Node):                             #TempSubscriberというノードを定義
    
#     def __init__(self):                                 #コンストラクタ

#         super().__init__('temp_subscriber')             #親クラスの __init__() を呼び出す

#         self.subscription = self.create_subscription(   #subscriberの作成
#             Float32,                                    #データ型
#             'temperature',                              #topic名
#             self.callback,                              #データ受信で実行する関数
#             10                                          #最大10件まで（＝1秒毎に飛んでくるデータを10件までは記憶できる）
#         )

#     def callback(self, msg):                            #コールバック関数（Topic受信時に（データが届いたら）呼ばれる）

#         self.get_logger().info(                         #ログ表示
#             f'Received={msg.data:.1f}'                  #f文字列
#         )


# def main(args=None):                                    #Main関数

#     rclpy.init(args=args)                               #ROS2通信の初期化

#     node = TempSubscriber()                             #ノード作成

#     rclpy.spin(node)                                    #受信待ちループ（データ来た？データ来た？を繰り返す）

#     node.destroy_node()                                 #終了処理
#     rclpy.shutdown()


# if __name__ == '__main__':                              #おまじない（Pythonファイルを直接実行したときにmain関数を呼び出す）
#     main()

# ####################################################
# #課題14：Subscriberで閾値判定を作成する。
# #       上記で作成したSubscriberを改良して、温度異常監視を作成する。
# #       10℃未満 → 低温異常
# #       30℃超 → 高温異常
# ####################################################
# class TempSubscriber(Node):                             #ノードの定義（ROS2のノードクラスを継承）

#     def __init__(self):                                 #コンストラクタ（ノード生成時に自動実行される）
#         super().__init__('temp_subscriber')             #親クラスの __init__() を呼び出す

#         self.subscription = self.create_subscription(   #subscriberの作成（＝temperatureトピックにFloat32が届いたらcallback()を実行してね）
#             Float32,                                    #データ型
#             'temperature',                              #topic名
#             self.callback,                              #コールバック関数呼び出し
#             10                                          #キューサイズ
#         )

#     def callback(self, msg):                            #コールバック関数の中身（例.Publisherが「msg.data = 35.2」を送ると、callback(msg)が呼ばれます）

#         temp = msg.data                                 #受信データの取得(例.「35.2」が入ります)

#         self.get_logger().info(                         #温度表示
#             f'Received={temp:.1f}°C'                    #出力例.[INFO] Received=35.2°C
#         )

#         if temp > 30.0:                                 #30℃を超えた場合
#             self.get_logger().error(                    #高温エラー処理
#                 f'High Temperature Alarm! {temp:.1f}°C' #出力例.[ERROR] High Temperature Alarm! 35.2°C
#             )

#         elif temp < 10.0:                               #10℃を下回った場合
#             self.get_logger().warning(                  #低温ワーニング処理
#                 f'Low Temperature Alarm! {temp:.1f}°C'  #出力例.[WARN] Low Temperature Alarm! 5.8°C
#             )

# def main(args=None):                                    #main関数
#     rclpy.init(args=args)                               #ROS2通信の初期化

#     node = TempSubscriber()                             #Subscriberの呼び出し

#     rclpy.spin(node)                                    #データの受信ループ

#     node.destroy_node()                                 #終了処理
#     rclpy.shutdown()

# if __name__ == '__main__':                              #おまじない
#     main()

# ####################################################
# #課題14-1：連続異常監視
# #             上記で作成したSubscriberを改良して、連続異常監視を作成する。
# #           　2回連続以上を検知する。
# ####################################################
# class TempSubscriber(Node):

#     def __init__(self):
#         super().__init__('temp_subscriber')
#         self.high_temp_count = 0                        #上限側の異常回数カウント用にsubscriberの外側で定義する
#         self.low_temp_count = 0                         #下限側の異常回数カウント用にsubscriberの外側で定義する
#         self.subscription = self.create_subscription(
#             Float32,
#             'temperature',
#             self.callback,
#             10
#         )

#     def callback(self, msg):

#         temp = msg.data

#         self.get_logger().info(
#             f'Received={temp:.1f}°C'
#         )

#         if temp > 30.0:

#             self.get_logger().error(
#                 f'High Temperature Alarm! {temp:.1f}°C'
#             )

#             self.high_temp_count += 1                   #異常を検知した場合はカウントアップ

#             if self.high_temp_count >= 2:               #上限側の異常検知2回目の判定
#                 self.get_logger().error(                #高温エラー処理
#                     'Continuous High Temperature Alarm'
#                 )

#         else:
#             self.high_temp_count = 0                    #2回目でない場合はカウントを0に戻す


#         if temp < 10.0:
            
#             self.get_logger().warning(
#                 f'Low Temperature Alarm! {temp:.1f}°C'
#             )

#             self.low_temp_count += 1                    #異常を検知した場合はカウントアップ
            
#             if self.low_temp_count >= 2:                #下限側の異常検知2回目の判定
#                 self.get_logger().error(                #低温エラー処理
#                     'Continuous low Temperature Alarm'
#                 )
#         else:
#             self.low_temp_count = 0                     #2回目でない場合はカウントを0に戻す


# def main(args=None):
#     rclpy.init(args=args)

#     node = TempSubscriber()

#     rclpy.spin(node)

#     node.destroy_node()

#     rclpy.shutdown()


# if __name__ == '__main__':
#     main()

# ####################################################
# #課題14-2：通信断監視
# #             Publisherの停止を検知。
# #           　Publisherからの通知が5秒間来なければ通信断発生と表示させる。
# ####################################################
# class TempSubscriber(Node):

#     def __init__(self):                                 #コンストラクタ
#         super().__init__('temp_subscriber')

       
#         self.last_received_time = time.time()            # 最後に受信した時刻

#         self.subscription = self.create_subscription(
#             Float32,
#             'temperature',
#             self.callback,                              #コールバック関数を呼ぶ
#             10
#         )

#         self.timer = self.create_timer(                 # 1秒ごとに通信監視
#             1.0,
#             self.check_timeout                          #タイムアウト判定関数を呼ぶ
#         )

#     def callback(self, msg):

#         temp = msg.data

        
#         self.last_received_time = time.time()           # 受信したら時刻更新

#         self.get_logger().info(
#             f'Received={temp:.1f}°C'                    #温度表示
#         )

#     def check_timeout(self):                            #タイムアウト判定関数

#         now = time.time()                               #現在時刻を秒単位で取得

        
#         if now - self.last_received_time > 3.0:         # 3秒以上受信なしかの判定

#             self.get_logger().error(                    #受信がない場合のエラー処理
#                 'Communication Timeout!'                
#             )


# def main(args=None):

#     rclpy.init(args=args)                               #初期化

#     node = TempSubscriber()                             #subscriberの呼び出し

#     rclpy.spin(node)                                    #データまだ？のループ

#     node.destroy_node()                                 #終了処理
#     rclpy.shutdown()


# if __name__ == '__main__':
#     main()

####################################################
#追加課題14-3：温度異常ログ保存
#             温度異常検知時にCSVへ保存します。
####################################################
class TempSubscriber(Node):                             #TempSubscriberというノードを定義
    
    def __init__(self):                                 #コンストラクタ

        super().__init__('temp_subscriber')             #親クラスの __init__() を呼び出す

        self.high_temp_count = 0                        #カウンタ初期化
        self.low_temp_count = 0

        with open(                                      #CSVヘッダ作成
            'temperature_log.csv',
            'w',
            newline='',
            encoding='utf-8'
        )as f:
            writer = csv.writer(f)

            writer.writerow(
                [
                    'timestamp',
                    'temperture',
                    'status'
                ]
            )

        self.subscription = self.create_subscription(   #subscriberの作成
            Float32,                                    #データ型
            'temperature',                              #topic名
            self.callback,                              #データ受信で実行する関数
            10                                          #最大10件まで（＝1秒毎に飛んでくるデータを10件までは記憶できる）
        )


    def callback(self, msg):                            #コールバック関数（Topic受信時に（データが届いたら）呼ばれる）

        temp = msg.data

        self.get_logger().info(                         #ログ表示
            f'Received={msg.data:.1f}'                  #f文字列
        )

        if temp > 30.0:
            self.get_logger().error(
                f'High Temperatuure Alarm!{temp:.1f}℃'
            )
            self.save_log(
                temp,
                'HIGH'
            )

        elif temp < 10.0:
            self.get_logger().warning(
                f'Low Temperatuer Alarm!{temp:.1f}℃'
            )
            self.save_log(
                temp,
                'LOW'
            )


    def save_log(self, temp, status):                   #温度異常時のログを保存する関数
            
            print("save_log called")                    #デバッグログ

            timestamp = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            with open(
                'temperature_log.csv',
                'a',
                newline='',
                encoding='utf-8'
            )as f:
                writer = csv.writer(f)
                writer.writerow(
                    [
                        timestamp,
                        temp,
                        status
                    ]
                )   


def main(args=None):                                    #Main関数

    rclpy.init(args=args)                               #ROS2通信の初期化

    node = TempSubscriber()                             #ノード作成

    rclpy.spin(node)                                    #受信待ちループ（データ来た？データ来た？を繰り返す）

    node.destroy_node()                                 #終了処理
    rclpy.shutdown()


if __name__ == '__main__':                              #おまじない（Pythonファイルを直接実行したときにmain関数を呼び出す）
    main()



