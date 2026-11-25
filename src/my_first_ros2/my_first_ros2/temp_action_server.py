import rclpy                                            #ROS2の機能をPythonから使いための基本ライブラリ
from rclpy.node import Node                             #rclpy.nodeの中からROS2のノードを使うための設計図を読込む

import time                                             #時間に関する処理を行うためのライブラリ
from rclpy.action import ActionServer                   #ros2のactionサーバーを使うためのクラス
from example_interfaces.action import Fibonacci         #ros2標準のaction定義

import random
# ####################################################
# #課題16：モーター回転シミュレーション
# #       　clientがモーターの回転要求を出して、serverが回転開始→進捗状況→回転終了をclientに返す。
# ####################################################
# class MotorActionServer(Node):                          #ノードクラスの定義

#     def __init__(self):                                 #コンストラクタ
#         super().__init__('motor_action_server')         #ROS通信上の名前をmotor_action_serverに設定

#         self.action_server = ActionServer(              #actionサーバの中身
#             self,                                       #actionサーバーを保有するノードを指定
#             Fibonacci,                                  #データ型
#             'motor_rotate',                             #action名
#             self.execute_callback                       #クライアントから要求が来た際に実行する関数
#         )

#     def execute_callback(self, goal_handle):            #コールバック関数の定義（goal_handleにクライアントからの要求が入っています）

#         self.get_logger().info('モーター回転開始')       #開始時のログを表示

#         feedback = Fibonacci.Feedback()                 #進捗通知用のデータ領域を作成

#         for i in range(1, 11):                          #1～10までループ開始

#             time.sleep(1)                               #1秒待機

#             percent = i * 10                            #進捗率の計算

#             feedback.sequence = [percent]               #計算した進捗率をfeedbackに格納

#             goal_handle.publish_feedback(feedback)      #クライアントへ進捗通知を送信

#             self.get_logger().info(                     #サーバー側にも進捗を表示
#                 f'進捗 {percent}%'
#             )                                           #ループ終了

#         goal_handle.succeed()                           #actionの成功を宣言

#         result = Fibonacci.Result()                     #最終結果用のデータ領域を作成

#         result.sequence = [100]                         #最終結果を設定

#         self.get_logger().info(                         #終了時のログを表示
#             '回転完了'
#         )

#         return result                                   #結果を返す


# def main(args=None):                                    #Main関数の定義

#     rclpy.init(args=args)                               #初期化

#     node = MotorActionServer()                          #ノードの呼び出し

#     rclpy.spin(node)                                    #終了処理
#     rclpy.shutdown()


# if __name__ == '__main__':                              #おまじない
#     main()

####################################################
#課題16ｰ1：設備検査シミュレーション(Action通信版)
#       　client:設備検査要求→server:検査開始（進捗表示）→server:検査完了→server:結果判定→client:結果返却
####################################################
class EquipmentInspectionServer(Node):                  #ノードクラスの定義

    def __init__(self):                                 #コンストラクタ

        super().__init__('equipment_inspection_server') #ノード名の設定

        self.action_server = ActionServer(              #ノードの中身を定義してselfのメンバ変数に代入
            self,                                       #現在のノード
            Fibonacci,                                  #データ型
            'equipment_inspection',                     #アクション名（client側と統一）
            self.execute_callback                       #コールバック関数の呼び出し
        )

    def execute_callback(self, goal_handle):            #コールバック関数の定義

        self.get_logger().info(                         #ROS2のログ（設備検査開始）を画面に表示する処理
            '設備検査開始'
        )

        feedback = Fibonacci.Feedback()                 #クライアントへ途中経過（フィードバック）を送るためのメッセージオブジェクトを作成

        for i in range(1, 6):                           #1~5までのループ

            time.sleep(2)                               #2秒待機

            progress = i * 20                           #進捗率の計算

            feedback.sequence = [progress]              #進捗率の計算結果をfeedbackに格納

            goal_handle.publish_feedback(               #serverからclientに途中経過を送信
                feedback
            )

            self.get_logger().info(                     #server側のターミナルにも検査進捗を表示
                f'検査進捗 {progress}%'
            )

        goal_handle.succeed()                           #Actionの成功を宣言

        result = Fibonacci.Result()                     #最終結果を送るためのメッセージオブジェクトを作成

        inspection_result = random.choice(              #正常/異常のリストからランダムに選択
            [0, 1]
        )

        result.sequence = [inspection_result]           #上記の結果を配列にしてresult.sequenceに格納

        if inspection_result == 0:                      #inspection_resultが0の場合

            self.get_logger().info(                     #設備正常を表示
                '設備正常'
            )

        else:                                           #inspection_resultが1の場合     

            self.get_logger().warn(                     #異常検知を表示
                '異常検知'
            )

        return result                                   #結果を返却


def main(args=None):                                    #main関数の定義

    rclpy.init(args=args)                               #初期化

    node = EquipmentInspectionServer()                  #ノードクラスの呼び出し

    rclpy.spin(node)                                    #clientからの依頼待ちループ

    rclpy.shutdown()                                    #ノードの終了


if __name__ == '__main__':                              #おまじない
    main()