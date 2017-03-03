#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flex_nav_flexbe_states.move_distance_state import MoveDistanceState
from flex_nav_flexbe_states.clear_costmaps_state import ClearCostmapsState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon Jan 09 2017
@author: Justin Willis
'''
class TurtlebotSimpleRecoverySM(Behavior):
    '''
    Stops the robot, clears the cost map, and backs up
    '''


    def __init__(self):
        super(TurtlebotSimpleRecoverySM, self).__init__()
        self.name = 'Turtlebot Simple Recovery'

        # parameters of this behavior

        # references to used behaviors

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]

		# [/MANUAL_INIT]

        # Behavior comments:



    def create(self):
        # x:418 y:118, x:83 y:190
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]

		# [/MANUAL_CREATE]


        with _state_machine:
            # x:94 y:63
            OperatableStateMachine.add('Stop',
                                        MoveDistanceState(target_time=1.0, distance=0.0, cmd_topic='stamped_cmd_vel_mux/input/navi', odometry_topic='mobile_base/odom'),
                                        transitions={'done': 'Backup', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

            # x:294 y:63
            OperatableStateMachine.add('Backup',
                                        MoveDistanceState(target_time=1, distance=-0.25, cmd_topic='stamped_cmd_vel_mux/input/navi', odometry_topic='mobile_base/odom'),
                                        transitions={'done': 'Clear Costmap', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

            # x:291 y:178
            OperatableStateMachine.add('Clear Costmap',
                                        ClearCostmapsState(costmap_topics=['high_level_planner/clear_costmap','low_level_planner/clear_costmap']),
                                        transitions={'done': 'finished', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]

	# [/MANUAL_FUNC]
