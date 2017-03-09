#!/usr/bin/env python
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flex_nav_flexbe_states.clear_costmaps_state import ClearCostmapsState
from flex_nav_flexbe_states.get_path_state import GetPathState
from flexbe_states.operator_decision_state import OperatorDecisionState
from flex_nav_flexbe_states.follow_path_state import FollowPathState
from flex_nav_turtlebot_flexbe_states.turtlebot_status_state import TurtlebotStatusState
from flex_nav_turtlebot_flexbe_behaviors.turtlebot_simple_recovery_sm import TurtlebotSimpleRecoverySM
from flexbe_states.log_state import LogState
from flex_nav_flexbe_states.get_pose_state import GetPoseState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon Jan 09 2017
@author: Josh Cohen
'''
class TurtlebotFlexPlannerSM(Behavior):
    '''
    Uses Flexible Navigation to control the Turtlebot robot
    '''


    def __init__(self):
        super(TurtlebotFlexPlannerSM, self).__init__()
        self.name = 'Turtlebot Flex Planner'

        # parameters of this behavior

        # references to used behaviors
        self.add_behavior(TurtlebotSimpleRecoverySM, 'Turtlebot Simple Recovery')

        # Additional initialization code can be added inside the following tags
        # [MANUAL_INIT]

		# [/MANUAL_INIT]

        # Behavior comments:



    def create(self):
        # x:839 y:185, x:1163 y:18
        _state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

        # Additional creation code can be added inside the following tags
        # [MANUAL_CREATE]

		# [/MANUAL_CREATE]

        # x:33 y:240, x:133 y:240, x:322 y:248, x:233 y:240, x:412 y:246, x:547 y:181, x:538 y:99, x:536 y:247
        _sm_container_0 = ConcurrencyContainer(outcomes=['finished', 'failed', 'danger'], input_keys=['plan'], conditions=[
                                        ('failed', [('DWA', 'failed')]),
                                        ('finished', [('DWA', 'done')]),
                                        ('failed', [('DWA', 'preempted')]),
                                        ('danger', [('Safety', 'cliff')]),
                                        ('danger', [('Safety', 'bumper')])
                                        ])

        with _sm_container_0:
            # x:101 y:78
            OperatableStateMachine.add('DWA',
                                        FollowPathState(topic="low_level_planner"),
                                        transitions={'done': 'finished', 'failed': 'failed', 'preempted': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off, 'preempted': Autonomy.Off},
                                        remapping={'plan': 'plan'})

            # x:299 y:68
            OperatableStateMachine.add('Safety',
                                        TurtlebotStatusState(bumper_topic='mobile_base/events/bumper', cliff_topic='mobile_base/events/cliff'),
                                        transitions={'bumper': 'danger', 'cliff': 'danger'},
                                        autonomy={'bumper': Autonomy.Off, 'cliff': Autonomy.Off})



        with _state_machine:
            # x:40 y:24
            OperatableStateMachine.add('ClearCostmap',
                                        ClearCostmapsState(costmap_topics=['high_level_planner/clear_costmap','low_level_planner/clear_costmap']),
                                        transitions={'done': 'Receive Goal', 'failed': 'failed'},
                                        autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})

            # x:206 y:179
            OperatableStateMachine.add('Receive Path',
                                        GetPathState(planner_topic="high_level_planner"),
                                        transitions={'planned': 'ExecutePlan', 'empty': 'Continue', 'failed': 'Continue'},
                                        autonomy={'planned': Autonomy.Off, 'empty': Autonomy.Low, 'failed': Autonomy.Low},
                                        remapping={'goal': 'goal', 'plan': 'plan'})

            # x:194 y:274
            OperatableStateMachine.add('ExecutePlan',
                                        OperatorDecisionState(outcomes=["yes","no"], hint="Execute the current plan?", suggestion="yes"),
                                        transitions={'yes': 'Container', 'no': 'Continue'},
                                        autonomy={'yes': Autonomy.High, 'no': Autonomy.Full})

            # x:406 y:270
            OperatableStateMachine.add('Container',
                                        _sm_container_0,
                                        transitions={'finished': 'Log Success', 'failed': 'New Plan', 'danger': 'Log Fail'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'danger': Autonomy.Inherit},
                                        remapping={'plan': 'plan'})

            # x:395 y:102
            OperatableStateMachine.add('Continue',
                                        OperatorDecisionState(outcomes=["yes","no","recover"], hint="Continue planning to new goal?", suggestion="yes"),
                                        transitions={'yes': 'Receive Goal', 'no': 'finished', 'recover': 'LogRecovery'},
                                        autonomy={'yes': Autonomy.High, 'no': Autonomy.Full, 'recover': Autonomy.Full})

            # x:1036 y:232
            OperatableStateMachine.add('Turtlebot Simple Recovery',
                                        self.use_behavior(TurtlebotSimpleRecoverySM, 'Turtlebot Simple Recovery'),
                                        transitions={'finished': 'AutoReplan', 'failed': 'failed'},
                                        autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

            # x:414 y:182
            OperatableStateMachine.add('Log Success',
                                        LogState(text="Success!", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'Continue'},
                                        autonomy={'done': Autonomy.Off})

            # x:586 y:274
            OperatableStateMachine.add('Log Fail',
                                        LogState(text="Path execution failure", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'Recover'},
                                        autonomy={'done': Autonomy.Off})

            # x:960 y:70
            OperatableStateMachine.add('Log Recovered',
                                        LogState(text="Re-plan after recovery", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'New Plan'},
                                        autonomy={'done': Autonomy.Off})

            # x:772 y:71
            OperatableStateMachine.add('New Plan',
                                        GetPathState(planner_topic="high_level_planner"),
                                        transitions={'planned': 'Container', 'empty': 'Receive Goal', 'failed': 'Continue'},
                                        autonomy={'planned': Autonomy.Off, 'empty': Autonomy.Off, 'failed': Autonomy.Off},
                                        remapping={'goal': 'goal', 'plan': 'plan'})

            # x:206 y:72
            OperatableStateMachine.add('Receive Goal',
                                        GetPoseState(topic='flex_nav_global/goal'),
                                        transitions={'done': 'Receive Path'},
                                        autonomy={'done': Autonomy.Low},
                                        remapping={'goal': 'goal'})

            # x:709 y:273
            OperatableStateMachine.add('Recover',
                                        OperatorDecisionState(outcomes=["yes","no"], hint="Should we attempt recovery?", suggestion="yes"),
                                        transitions={'yes': 'LogRecovery', 'no': 'finished'},
                                        autonomy={'yes': Autonomy.High, 'no': Autonomy.Full})

            # x:887 y:236
            OperatableStateMachine.add('LogRecovery',
                                        LogState(text="Starting recovery behavior", severity=Logger.REPORT_HINT),
                                        transitions={'done': 'Turtlebot Simple Recovery'},
                                        autonomy={'done': Autonomy.Off})

            # x:973 y:159
            OperatableStateMachine.add('AutoReplan',
                                        OperatorDecisionState(outcomes=["yes","no"], hint="Re-plan to current goal?", suggestion=None),
                                        transitions={'yes': 'Log Recovered', 'no': 'Continue'},
                                        autonomy={'yes': Autonomy.High, 'no': Autonomy.Full})


        return _state_machine


    # Private functions can be added inside the following tags
    # [MANUAL_FUNC]

	# [/MANUAL_FUNC]
