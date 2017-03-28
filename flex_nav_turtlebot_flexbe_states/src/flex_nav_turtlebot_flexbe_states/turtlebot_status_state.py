#!/usr/bin/env python

###############################################################################
#  Copyright (c) 2016
#  Capable Humanitarian Robotics and Intelligent Systems Lab (CHRISLab)
#  Christopher Newport University
#
#  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are met:
#
#    1. Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#
#    2. Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
#    3. Neither the name of the copyright holder nor the names of its
#       contributors may be used to endorse or promote products derived from
#       this software without specific prior written permission.
#
#       THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#       "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#       LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
#       FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
#       COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
#       INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
#       BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#       LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#       CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
#       LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY
#       WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#       POSSIBILITY OF SUCH DAMAGE.
###############################################################################

import rospy

from flexbe_core import EventState, Logger
from flexbe_core.proxy import ProxySubscriberCached

from kobuki_msgs.msg import BumperEvent, CliffEvent

class TurtlebotStatusState(EventState):
    """
    The state monitors the Kobuki turtlebot bumper and cliff sensors and will
    return an outcome if a one is activated.

    -- bumper_topic    string    The topic that the bumper events are published
    -- cliff_topic     string    The topic that the cliff events are published

    <= bumper    A bumper was activated
    <= cliff     The cliff sensor
    """

    def __init__(self, bumper_topic = 'mobile_base/events/bumper',
                       cliff_topic  = 'mobile_base/events/cliff'):

        super(TurtlebotStatusState, self).__init__(outcomes = ['bumper', 'cliff'])

        self._bumper_topic = bumper_topic
        self._cliff_topic = cliff_topic
        self._bumper_sub = ProxySubscriberCached({self._bumper_topic: BumperEvent})
        self._cliff_sub = ProxySubscriberCached({self._cliff_topic: CliffEvent})
        self._return = None # Handle return in case outcome is blocked by low autonomy

    def execute(self, userdata):
        if self._bumper_sub.has_msg(self._bumper_topic):
            sensor = self._bumper_sub.get_last_msg(self._bumper_topic)
            self._bumper_sub.remove_last_msg(self._bumper_topic)

            if sensor.state > 0:
                Logger.logwarn('Bumper %d contact' % (sensor.bumper))
                self._return = 'bumper'

        if self._cliff_sub.has_msg(self._cliff_topic):
            sensor = self._cliff_sub.get_last_msg(self._cliff_topic)
            self._cliff_sub.remove_last_msg(self._cliff_topic)
            if sensor.state > 0:
                Logger.logwarn('Cliff alert')
                self._return = 'cliff'

        return self._return

    def on_enter(self, userdata):
        self._return = None # Clear the completion flag
