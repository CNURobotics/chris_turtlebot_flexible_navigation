Chris Turtlebot Flexible Navigation
================================

## Introduction

CHRISLab specific implementations of the [ROS] and [FlexBE]-based [Flexible Navigation] ([Wiki]) for use with the Kobuki-based Turtlebot.

This repository contains code that interfaces with the [CHRISLab Turtlebot] system, and the [FlexBE System] and new open-source CHRISLab [Flexible Navigation] system.

Installation and Setup
----------------------

This package has a number of dependencies.  The quickest, and easiest method to get a demonstration up and running, is to follow the [CHRISLab Installation] below.  This quickly sets up the entire CHRISLab system in a separate workspace.

1) Ensure that you are running a recent ROS version; this system is tested on `ros-kinetic-desktop-full`.  See [ROS Installation] for more information.

2) Follow the [CHRISLab Installation] guide
* This will install the entire system in a new workspace. Once you build, you can run the Gazebo simulation based demonstration described below.
* For this system, you need to run `./rosinstall/install_scripts/install_chris_turtlebot.sh` from the root workspace.

3) Make sure the [FlexBE System], which will be installed as part of the [CHRISLab Installation], is properly set up.  It requires the [FlexBE App Installation] into the Chromium browser.

4) [FlexBE] must be configured to point to the proper repos after the [CHRISLab Installation] is complete and built.
 This configuration can be completed once FlexBE is started below.

 * Workspace
  * Behaviors Folder: `~/CHRISLab/src/chris_turtlebot_flexible_navigation/flex_nav_turtlebot_behaviors`
  * flexbe_behaviors: `~/CHRISLab/src/chris_turtlebot_flexible_navigation/flex_nav_turtlebot_flexbe_behaviors`

 * State Libraries
  * `~/CHRISLab/src/flexbe_behavior_engine/flexbe_states/src/flexbe_states`
  * `~/CHRISLab/src/generic_flexbe_states/flexbe_navigation_states/src/flexbe_navigation_states`
  * `~/CHRISLab/src/generic_flexbe_states/flexbe_utility_states/src/flexbe_utility_states`
  * `~/CHRISLab/src/flexible_navigation/flex_nav_flexbe_states/src/flex_nav_flexbe_states`
  * `~/CHRISLab/src/chris_turtlebot_flexible_navigation/flex_nav_turtlebot_flexbe_states/src/flex_nav_turtlebot_flexbe_states`


## Operation
---------

The following directions are for a simple demonstration on a single ROS network.

`roscore`
 * Required for ROS network
 * Start a separate ROS core to simplify startup and re-running nodes as needed


### Start the simulated robot


 `roslaunch chris_world_models gazebo_simple_creech_world.launch`
 * This is a simple world with obstacles; not robots are included.
 * Other launch files include the Willow Garage office model

 `roslaunch chris_turtlebot_bringup chris_turtlebot_gazebo.launch`
 * Starts the simulated CHRISlab Turtlebot with a Hokuyo URG-04LX Lidar and Kinect 3D Sensor
 * Places the simulated robot in existing Gazebo simulation that must be started first.


### Start localization

 There are several options; choose one:


 `roslaunch chris_turtlebot_navigation fake_localization_demo.launch`
  * This launches a fake localization with empty mapping

 `roslaunch chris_turtlebot_navigation amcl*.launch`
  * AMCL uses Adaptive Monte Carlo Localization with respect to a known map
  * Use the launch file with map corresponding to the Gazebo world (maps are located in common chris_world_models package)
  * For Creech world use `roslaunch chris_turtlebot_navigation amcl_creech_world.launch`


  `roslaunch chris_turtlebot_navigation gmapping_demo.launch`
  * This uses Simultaneous Localization and Mapping (SLAM) to build a map during navigation.


 *NOTE:* For AMCL and gmapping, the maps must be consistent with SBPL-based planners configured in this setup.

### Visualization

 `roslaunch flex_nav_turtlebot_bringup turtlebot_flex_nav_rviz.launch`
  * A standard view of Turtlebot and sensor data, with maps, and paths displayed
  * Topic names are customized in this configuration to match this demo

### Startup of Flexible Navigation

Start both planning and control nodes, and the FlexBE behavior engine

`roslaunch flex_nav_turtlebot_bringup flex.launch`
 * This starts the planning and control nodes.
 * This version uses a 2-layer planner as a demonstration.
  * Only a simple set of SBPL motion primitives is included in this version, and will be refined in the future.

`roslaunch flex_nav_turtlebot_flexbe_behaviors flex_nav_turtlebot_behavior_testing.launch`
  * This starts the FlexBE engine and FlexBE UI (Chromium App)
  * Load the `FlexPlanner` behavior


These launch files may also be used with different `robot_namespaces`; different namespaces require different ports to be specified for `flex_nav_turtlebot_behavior_testing.launch`.


After start up, all control is through the FlexBE UI.  Load the `Turtlebot Flex Planner` behavior, and run.  The system asks for a 2D Nav Pose input via RViz, and then asks for confirmation of the initial global plan.  If the supervisor chooses to execute the plan, the state transitions to a concurrent node that uses an online multilayer planner to refine the plans as the robot moves, and also monitors the Create bumper status for collision.

[ROS]: http://www.ros.org
[FlexBE]: https://flexbe.github.io
[Flexible Navigation]: https://github.com/CNURobotics/flexible_navigation
[Wiki]: http://wiki.ros.org/flexible_navigation
[CHRISLab Turtlebot]: https://github.com/CNURobotics/chris_ros_turtlebot
[FlexBE System]: https://github.com/team-vigir/flexbe_behavior_engine
[CHRISLab Installation]: https://github.com/CNURobotics/chris_install
[FlexBE App Installation]: http://philserver.bplaced.net/fbe/download.php
[ROS Installation]: http://wiki.ros.org/kinetic/Installation
