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
            self.missions["positioning"].process_event(StartEvent())
            self.state +=1
