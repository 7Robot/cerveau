# -*- coding: utf-8 -*-
'''
Created on 27 avr. 2012
'''

from missions.mission import Mission
from events.internal import StartEvent

class StartMission(Mission):
    def __init__(self, robot):
        super(self.__class__,self).__init__(robot)

    def process_event(self, event):
        if self.state == 0:
            self.robot.send_can("rangefinder 1 threshold 1800")
            self.robot.send_can("rangefinder 2 threshold 1800")
            self.missions["odo"].broadcast()
            self.robot.send_can("turret unmute")
            self.robot.send_can("turret on")
            #self.missions["positioning"].process_event(StartEvent())
            self.state += 1

        elif self.state == 1:
            if event.name == "bump" and event.state == "open":
                self.robot.forward(-4000)
