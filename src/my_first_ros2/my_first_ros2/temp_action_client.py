import rclpy                                        #ROS2のPython用ライブラリ
from rclpy.node import Node                         #ROS2のノードを使うためのクラス
import time                                         #時間に関する処理を行うためのライブラリ

from rclpy.action import ActionClient               #action clientを使うためのクラス
from example_interfaces.action import Fibonacci     #action通信で使用するメッセージ型

# ####################################################
# #課題16：モーター回転シミュレーション
# #       　clientがモーターの回転要求を出して、serverが回転開始→進捗状況→回転終了をclientに返す。
# ####################################################
# class MotorActionClient(Node):                      #ノードクラスを定義

#     def __init__(self):                             #コンストラクタ

#         super().__init__('motor_action_client')     #ROS通信上の呼び名をmotor_action_clientに設定

#         self.client = ActionClient(                 #クライアントの中身
#             self,                                   #ノード指定
#             Fibonacci,                              #データ型
#             'motor_rotate'                          #action名
#         )

#     def send_goal(self):                            #目標をサーバーに送るメソッド

#         self.client.wait_for_server()               #action serverが起動するまで待機

#         goal = Fibonacci.Goal()                     #Goalメッセージを作成

#         goal.order = 100                            #メンバ変数のオーダーに100を代入

#         self.future = self.client.send_goal_async(  #Goalを非同期送信
#             goal,                                   
#             feedback_callback=self.feedback_callback#進捗通知が来たらfeedback_callback関数を呼ぶ
#         )

#         self.future.add_done_callback(              #
#             self.goal_response_callback             #
#         )

#     def feedback_callback(                          #サーバーから進捗通知を受信したときに呼ばれる関数
#         self,
#         feedback_msg
#     ):

#         progress = feedback_msg.feedback.sequence[0]#Feedbackから進捗率を取り出す

#         print(f'進捗: {progress}%')                 #進捗率を表示

#     def goal_response_callback(                     #server側からGoalを受け付けた際に呼ばれる関数
#         self,
#         future
#     ):

#         goal_handle = future.result()               #Goalを管理するハンドルを取得

#         result_future = goal_handle.get_result_async()  #最終結果を待つ予約

#         result_future.add_done_callback(            #完了したらresult_callback関数を呼び出す
#             self.result_callback
#         )

#     def result_callback(                            #server側から最終結果を受信したときに呼ばれる関数
#         self,
#         future
#     ):

#         result = future.result().result             #結果データを取得

#         print(                                      #結果を表示
#             f'完了: {result.sequence[0]}%'
#         )

#         rclpy.shutdown()                            #ros2ノードを終了


# def main(args=None):                                #Main関数の定義

#     rclpy.init(args=args)                           #初期化

#     node = MotorActionClient()                      #ノードの呼び出し

#     node.send_goal()                                #関数呼び出し

#     rclpy.spin(node)                                #結果を受け取るためにループさせる


# if __name__ == '__main__':                          #おまじない
#     main()

####################################################
#課題16ｰ1：設備検査シミュレーション(Action通信版)
#       　client:設備検査要求→server:検査開始（進捗受取）→server:検査完了→server:結果判定→client:結果返却
####################################################
class EquipmentInspectionClient(Node):                  #クラス定義

    def __init__(self):                                 #コンストラクタ(クラスからオブジェクトを生成した瞬間に自動実行される関数)
                                                        #↑EquipmentInspectionClient()を実行すると自動実行されるためself＝Nodeの考えでOKとする。

        super().__init__(                                   #ノード名を'equipment_inspection_client'と名付ける
            'equipment_inspection_client'
        )

        self.client = ActionClient(                         #selfのclientというメンバ変数を定義して、ActionClientというオブジェクトを生成して中身を代入している
            self,                                           #現在のノード
            Fibonacci,                                      #データ型
            'equipment_inspection'                          #action名（server側と揃える）
        )


    def send_goal(self):                                #検査開始要求を送る関数を定義（内部でself.clientを使うためselfを引数で渡す）

        self.client.wait_for_server()                       #server側は起動するまで待機
                                                            #↑wait_for_server()は、self.clientに入れたActionClientの複数あるメソッド（＝オブジェクトが持つ操作）の内の１つ

        goal = Fibonacci.Goal()                             #Action Serverへ送る「依頼データ（Goal）」を作成
                                                            #↑Fibonacciのメッセージ型にはGoal、Feedback、Resultの３つが定義されており、その内の１つ

        goal.order = 1                                      #goalのorderに1を代入
                                                            #↑1つ上の処理が実行されるとgoalの下にorderオブジェクトが生成される

        future = self.client.send_goal_async(               #Server側にgoalを送信（async＝非同期）
                                                            #↑send_goal_asyncはAction ServerにGoal（依頼）を送信するためのメソッド

            goal,                                           #設備検査を開始してくださいという依頼をServerに送付
            feedback_callback=self.feedback_callback        #進捗受信用関数の呼び出し（serverから受信すると呼ばれる）
        )

        future.add_done_callback(                           #受付応答処理関数の呼び出し（上の処理でfutureに結果が入ったら、goal_response_callback() を自動実行）
            self.goal_response_callback
        )


    def feedback_callback(                              #進捗受信用関数の定義（進捗の応答を表示）
        self,
        feedback_msg
    ):

        progress = (feedback_msg.feedback.sequence[0])      #進捗取得（Serverからのフィードバックデータが入っているリストの先頭を取得してprogressに代入）

        print(f'検査進捗 : {progress}%')                    #画面上に進捗表示
            
        
    def goal_response_callback(self,future):            #受付応答処理関数の定義（受付結果待ち）

        goal_handle = future.result()                       #Action ServerがGoalを受け付けた結果（GoalHandleオブジェクト）を取得

        result_future = (                                   #Action Serverの最終結果(Result)を非同期で待ち始める
            goal_handle.get_result_async()                  #調査完了したら結果をくださいの処理
        )

        result_future.add_done_callback(                    #結果を受信したらコールバック関数を呼び出す
            self.result_callback
        )

    def result_callback(self,future):                   #コールバック関数の定義（検査結果の正常異常を表示）
        
        result = future.result().result                     #serverから返された結果をresultに格納

        if not result.sequence:                             #NULLチェック
            print("結果データが空です")
            rclpy.shutdown()
            return

        status = result.sequence[0]                         #resultリスト（配列）の先頭データを取り出して、変数 status に代入

        if status == 0:                                     #正常判定の場合、'【検査結果】設備正常'と表示

            print(
                '【検査結果】設備正常'
            )

        else:                                               #異常判定の場合、【検査結果】異常検知と表示

            print(
                '【検査結果】異常検知'
            )

        rclpy.shutdown()                                #ノード終了


def main(args=None):                                    #main関数を定義

    rclpy.init(args=args)                               #初期化

    node = EquipmentInspectionClient()                  #ノードクラスの呼び出し

    node.send_goal()                                    #検査開始の要求

    rclpy.spin(node)                                    #フィードバック待ち用のループ


if __name__ == '__main__':                              #おまじない
    main()