# -*- coding: utf-8 -*-
'''
Created on 27 avr. 2012
'''

from missions.mission import Mission
from events.internal import Start

class MissionRecalibration(Mission):

    def __init__(self):
        super(self.__class__,self).__init__(self, "Start")
        self.state = 1

    def processEvent(self, event):
        if self.state==1:
            self.missions["Recalibration"].process_event(Start())
            self.state +=1