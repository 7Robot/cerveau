# -*- coding: utf-8 -*-
'''
Created on 27 avr. 2012
'''

from missions.mission import Mission
from events.internal import Start

class MissionStart(Mission):

    def __init__(self):
        super(self.__class__,self).__init__("StartMission")
        self.state = 1

    def process_event(self, event):
        if self.state==1:
            self.missions["Recalibration"].process_event(Start())
            self.state +=1