import random                                       #乱数を作るためのPython標準ライブラリ
import rclpy                                        #ROS2のPythonライブラリ
from rclpy.node import Node                         #ROS2ノードを作るためのクラスを読み込む

from std_msgs.msg import Float32                    #メッセージ型を読み込む
from std_msgs.msg import String

# ####################################################
# #課題13：”Hello ROS2”を送信するPublisherを作成
# ####################################################
# class HelloPublisher(Node):

#     def __init__(self):
#         super().__init__('hello_publisher')

#         self.publisher_ = self.create_publisher(
#             String,
#             'hello_topic',
#             10
#         )

#         self.timer = self.create_timer(
#             1.0,
#             self.publish_message
#         )

#     def publish_message(self):

#         msg = String()

#         msg.data = "Hello ROS2"

#         self.publisher_.publish(msg)

#         self.get_logger().info(
#             f'Publishing: {msg.data}'
#         )


# def main(args=None):

#     rclpy.init(args=args)

#     node = HelloPublisher()

#     rclpy.spin(node)

#     node.destroy_node()

#     rclpy.shutdown()


# if __name__ == '__main__':
#     main()

####################################################
#課題13ｰ1：1秒おきに温度を送信するPublisherを作成
####################################################
class TempPublisher(Node):                          #TempPublisherというノードを定義
    def __init__(self):                             #ノード起動時に実行される処理
        super().__init__('temp_publisher')          #ノード名を’temp_publisher’に設定
        #Publisherを作成（データ型、トピック名、キューサイズ）
        self.publisher_ = self.create_publisher(    
            Float32,
            'temperature',
            10
        )

        #タイマーの作成（1秒ごとにpublish_temp関数を実行）
        self.timer = self.create_timer(             
            1.0,
            self.publish_temp
        )

    #温度送信処理関数（1秒ごとに呼ばれる関数の本体）
    def publish_temp(self):                     
        msg = Float32()                             #Float32型メッセージ作成
        msg.data = random.uniform(                  #乱数で温度データを作成
            1.0,
            40.0
        )

        #temperatureトピックへ送信
        self.publisher_.publish(msg)

        #ログを画面に表示
        self.get_logger().info(                 
            f'Temp={msg.data:.1f}'
        )
#main関数
def main(args=None):                                #プログラム開始処理

    rclpy.init(args=args)                           #ROS2を起動

    node = TempPublisher()                          #TempPublisherノードの作成

    rclpy.spin(node)                                #実行開始

    node.destroy_node()                             #終了処理
    rclpy.shutdown()

if __name__ == '__main__':                          #おまじない（Pythonファイルを直接実行したときにmain関数を呼び出す）
    main()
