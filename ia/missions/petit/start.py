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
            self.can.send("rangefinder 1 threshold 1800")
            self.can.send("rangefinder 2 threshold 1800")
            #self.missions["positioning"].process_event(StartEvent())
            self.state +=1
