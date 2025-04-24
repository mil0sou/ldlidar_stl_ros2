#!/usr/bin/env python3
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

'''
Parameter Description:
---
- Set laser scan direction: 
  1. Set counterclockwise, example: {'laser_scan_dir': True}
  2. Set clockwise,        example: {'laser_scan_dir': False}
- Angle crop setting, Mask data within the set angle range:
  1. Enable angle crop function:
    1.1. enable angle crop,  example: {'enable_angle_crop_func': True}
    1.2. disable angle crop, example: {'enable_angle_crop_func': False}
  2. Angle cropping interval setting:
  - The distance and intensity data within the set angle range will be set to 0.
  - angle >= 'angle_crop_min' and angle <= 'angle_crop_max' which is [angle_crop_min, angle_crop_max], unit is degrees.
    example:
      {'angle_crop_min': 135.0}
      {'angle_crop_max': 225.0}
      which is [135.0, 225.0], angle unit is degrees.
'''

def generate_launch_description():
  # Declare the port_name argument to allow setting it via command line
  port_name_arg = DeclareLaunchArgument(
      'port_name',
      default_value='/dev/ttyS0',  # Default to '/dev/ttyS0'
      description='Serial port name for the LD LiDAR'
  )

  # LDROBOT LiDAR publisher node
  ldlidar_node = Node(
      package='ldlidar_stl_ros2',
      executable='ldlidar_stl_ros2_node',
      name='LD06',
      output='screen',
      parameters=[
        {'product_name': 'LDLiDAR_LD06'},
        {'topic_name': 'scan'},
        {'frame_id': 'base_laser'},
        {'port_name': LaunchConfiguration('port_name')},  # Use the port_name argument
        {'port_baudrate': 230400},
        {'laser_scan_dir': True},
        {'enable_angle_crop_func': False},
        {'angle_crop_min': 135.0},
        {'angle_crop_max': 225.0}
      ]
  )

  # base_link to base_laser tf node
  base_link_to_laser_tf_node = Node(
    package='tf2_ros',
    executable='static_transform_publisher',
    name='base_link_to_base_laser_ld06',
    arguments=['0','0','0.18','0','0','0','base_link','base_laser']
  )

  # Define LaunchDescription variable
  ld = LaunchDescription()

  # Add the port_name argument to the launch description
  ld.add_action(port_name_arg)
  ld.add_action(ldlidar_node)
  ld.add_action(base_link_to_laser_tf_node)

  return ld
