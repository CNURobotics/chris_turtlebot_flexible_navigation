cmake_minimum_required(VERSION 2.8.3)
project(flex_nav_turtlebot_bringup)

# Load catkin and all dependencies required for this package
find_package(catkin REQUIRED COMPONENTS )

# What other packages will need to use this package
catkin_package(
    CATKIN_DEPENDS tf roscpp sensor_msgs flex_nav_planner flex_nav_controller flex_nav_flexbe_states flex_nav_turtlebot_flexbe_states
)


###########
## Build ##
###########


#############
## Install ##
#############


# Mark anything (useful) else for installation
install(DIRECTORY launch
        DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)

install(DIRECTORY param
        DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
