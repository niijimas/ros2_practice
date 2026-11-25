import random

import rclpy
from rclpy.node import Node

from std_msgs.msg import Float32


class TemperaturePublisher(Node):

    def __init__(self):
        super().__init__('temperature_pub')

        self.publisher = self.create_publisher(
            Float32,
            'temperature',
            10
        )

        self.timer = self.create_timer(
            1.0,
            self.publish_temperature
        )

    def publish_temperature(self):

        msg = Float32()

        msg.data = random.uniform(20.0, 80.0)

        self.publisher.publish(msg)

        self.get_logger().info(
            f'温度送信: {msg.data:.1f}℃'
        )


def main():
    rclpy.init()

    node = TemperaturePublisher()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()