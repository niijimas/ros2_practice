import rclpy
from rclpy.node import Node

from std_msgs.msg import Float32


class TemperatureMonitor(Node):

    def __init__(self):
        super().__init__('temperature_mot')

        self.subscription = self.create_subscription(
            Float32,
            'temperature',
            self.callback,
            10
        )

    def callback(self, msg):

        temp = msg.data

        if temp >= 70.0:

            self.get_logger().warn(
                f'高温異常: {temp:.1f}℃'
            )

        elif temp <= 30.0:

            self.get_logger().warn(
                f'低温異常: {temp:.1f}℃'
            )

        else:

            self.get_logger().info(
                f'正常: {temp:.1f}℃'
            )


def main():
    rclpy.init()

    node = TemperatureMonitor()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()