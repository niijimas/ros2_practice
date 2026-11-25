from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    return LaunchDescription([

        Node(
            package='my_first_ros2',
            executable='temperature_pub',
            output='screen'
        ),

        Node(
            package='my_first_ros2',
            executable='temperature_mot',
            output='screen'
        ),

        Node(
            package='my_first_ros2',
            executable='temperature_log',
            output='screen'
        )

    ])