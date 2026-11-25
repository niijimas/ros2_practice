import csv
import os
from datetime import datetime

import rclpy
from rclpy.node import Node

from std_msgs.msg import Float32


class TemperatureLogger(Node):

    def __init__(self):
        super().__init__('temperature_log')

        self.subscription = self.create_subscription(
            Float32,
            'temperature',
            self.callback,
            10
        )

    def callback(self, msg):

        file_exists = os.path.isfile(
            'temperature_log.csv'
        )                                               #CSVファイルが既に存在するか確認する。

        with open(
            'temperature_log.csv',
            'a',
            newline='',
            encoding='utf-8'
        ) as f:

            writer = csv.writer(f)

            if not file_exists:
                writer.writerow([
                    'timestamp',
                    'temperature'
                ])

            writer.writerow([
                datetime.now().strftime(
                    '%Y-%m-%d %H:%M:%S'
                ),
                f'{msg.data:.1f}'
            ])


def main():
    rclpy.init()

    node = TemperatureLogger()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()