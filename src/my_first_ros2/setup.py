from setuptools import find_packages, setup
from glob import glob

package_name = 'my_first_ros2'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name]
        ),
        (
            'share/' + package_name,
            ['package.xml']
        ),
        (
            'share/' + package_name + '/launch',
            glob('launch/*.launch.py')
        ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='niijimas',
    maintainer_email='niijimas@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
             'hello_pub = my_first_ros2.hello_pub:main',
             'temp_pub = my_first_ros2.temp_publisher:main',
             'temp_sub = my_first_ros2.temp_subscriber:main',
             'temp_server = my_first_ros2.temp_service_server:main',
             'temp_client = my_first_ros2.temp_service_client:main',
             'temp_a_server = my_first_ros2.temp_action_server:main',
             'temp_a_client = my_first_ros2.temp_action_client:main',
             'temperature_pub = my_first_ros2.temperature_pub:main',
             'temperature_mot = my_first_ros2.temperature_mot:main',
             'temperature_log = my_first_ros2.temperature_log:main',
        ],
    },
)
