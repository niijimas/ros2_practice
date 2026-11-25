import rclpy                                        #ROS2の機能をPythonから使いための基本ライブラリ
from rclpy.node import Node                         #rclpy.nodeの中からROS2のノードを使うための設計図を読込む
from example_interfaces.srv import Trigger          #service通信で使われる標準のデータ型triggerを読込む（リクエストは空でレスポンスとして成功フラグと文字列を返す形式）

import random                                       #Python標準の乱数ライブラリの読込み（ランダムな温度や振動数値を作るための模擬センサ用）

# ####################################################
# #課題15：温度取得service
# #       serverを温度センサ役と仮定して、Clientからの要求（現在温度は？）に応答（25.3℃）して、Clientが温度を表示（現在温度：25.3℃）する。
# ####################################################
# class TempServiceServer(Node):                      #読込んだノードクラス継承してTempServiceServerを定義

#     def __init__(self):                             #初期化メソッド（コンストラクタ）
#         super().__init__('temp_service_server')     #ROS2ネットワーク上でこのノードを'temp_service_server'という名前で登録

#         self.srv = self.create_service(             #serviceを作成してself.srvに格納
#             Trigger,                                #データ型
#             'get_temperature',                      #呼び出す際のサービス名
#             self.callback                           #リクエストが届いた際の実行するコールバック関数
#         )

#         self.get_logger().info(                     #ROS2標準のログ機能を使って、ターミナルの画面に「Temperature Service Ready（準備完了）」と情報（INFO）メッセージを表示
#             'Temperature Service Ready'             
#         )

#     def callback(self, request, response):          #'get_temperature'が呼び出された際のコールバック関数の中身

#         temp = 25.3                                 #固定値の25.3をtempに代入（本来はここで温度センサの値を読み取る）

#         response.success = True                     #返信用データ（Trigger 型）の success 項目に、「処理が成功した」という意味で True を代入
#         response.message = str(temp)                #返信用データの message 項目に、数値の 25.3 を str() で文字列 '25.3' に変換して代入（message は文字列しか入れられない決まりのため）

#         self.get_logger().info(                     #リクエストを受け取ったことをターミナルに表示
#             f'Request Received -> {temp:.1f}°C'     #（f'...' は変数を文字列に埋め込む記法で、{temp:.1f} は「小数点第1位まで表示する」という指定）
#         )

#         return response                             #値を詰めた response を呼び出し元のクライアントへ送り返して処理を完了


# def main(args=None):                                #Main関数の定義

#     rclpy.init(args=args)                           #ROS2通信システム全体の初期化

#     node = TempServiceServer()                      #serviceを呼び出す（実際のメモリ上にノードを作成して、この瞬間に__init__ が実行される）

#     rclpy.spin(node)                                #プログラムがすぐ終了してしまわないようにループ待機（クライアントからのリクエストを待ち続ける）

#     node.destroy_node()                             #Ctrl+C などで spin が終了したあと、作成したノードを破棄してメモリを解放
#     rclpy.shutdown()                                #ROS2の通信システムを正しく終了（シャットダウン）させる


# if __name__ == '__main__':                          #おまじない
#     main()

####################################################
#課題15-1：設備異常監視
#       リクエストが来るたびにセンサー値（今回はテスト用にランダムな温度と振動）をチェックし、閾値を超えていたら「異常（False）」を返す。
####################################################
class EquipmentMonitorServer(Node):

    def __init__(self):
        super().__init__('equipment_monitor_server')

        self.srv = self.create_service(                                                     # サービス名：check_equipment
            Trigger,
            'check_equipment',
            self.callback
        )

        # 異常判定のしきい値
        self.temp_limit = 60.0                                                              # 温度上限（℃）
        self.vibration_limit = 5.0                                                          # 振動上限（mm/s）

        self.get_logger().info('設備異常監視サーバーを起動しました。')                         #サーバーの準備が整ったことをターミナルにログ表示

    def callback(self, request, response):                                                  #コールバック関数
        # 模擬センサー値の取得（実際はここでセンサーから読み取る）
        current_temp = round(random.uniform(20.0, 85.0), 1)                                 #温度の模擬センサー
        current_vib = round(random.uniform(0.5, 6.5), 1)                                    #振動の模擬センサー

        # 異常判定ロジック
        errors = []                                                                         #検知した異常の内容を入れるための空のリスト
        if current_temp > self.temp_limit:                                                  #温度の閾値判定
            errors.append(f'高温異常({current_temp}℃)')                                     #温度が高い場合は'高温異常({current_temp}℃)'をerrorsリストに追加
        if current_vib > self.vibration_limit:                                              #振動の閾値判定
            errors.append(f'振動異常({current_vib}mm/s)')                                    #振動が大きい場合は'振動異常({current_vib}mm/s)'をerrorsリストに追加

        # レスポンスの作成
        if len(errors) == 0:                                                                 #errorsリストの中身を確認してエラー個数が0個か判定
            response.success = True                                                          #エラー個数が0この場合、返信用データのsuccessにtrueを代入
            response.message = f'正常稼働中 [温度:{current_temp}℃, 振動:{current_vib}mm/s]'  #返信用データのmessageに現在の温度と振動数値を代入
            self.get_logger().info(f'点検結果 -> 正常: {response.message}')                  #サーバー側のターミナルに正常だった旨のログを白文字で表示
        else:
            response.success = False                                                        #エラー個数が1以上の場合、返信用データのsuccessにFalseを代入
            error_detail = ' / '.join(errors)                                               #errorsリスト入っている異常内容を' / 'で繋げた文字列にする
            response.message = f'異常検知！ {error_detail}'                                  #返信用データのmessageに異常検知とその内容を代入
            self.get_logger().warn(f'点検結果 -> {response.message}')                        #サーバー側のターミナルに警告ログ（WARN）として強調表示

        return response                                                                     #判定結果の入ったresponseをクライアントに返却


def main(args=None):                                                                        #main関数を定義

    rclpy.init(args=args)                                                                   #ROS2の通信を初期化

    node = EquipmentMonitorServer()                                                         #サーバーからの結果をnodeに代入

    rclpy.spin(node)                                                                        #クラインとからのリクエストをループ待機

    node.destroy_node()                                                                     #終了処理
    rclpy.shutdown()


if __name__ == '__main__':                                                                  #おまじない
    main()

