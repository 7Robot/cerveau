# -*- coding: utf-8 -*-
'''
Created on 27 avr. 2012
'''

from missions.mission import Mission
from events.internal import StartEvent

class StartMission(Mission):
    def __init__(self, robot, can, ui):
        super(self.__class__,self).__init__(robot, can, ui)

    def process_event(self, event):
        if self.state == 0:
            self.state +=1
            self.can.send("rangefinder 1 threshold 2800")
            self.can.send("rangefinder 2 threshold 2800")
            self.can.send("rangefinder 8 threshold 2800")
            self.can.send("turret unmute")
            self.can.send("turret on")
            #self.missions["positioning"].process_event(StartEvent())
            self.missions["forward"].start(-15000)
