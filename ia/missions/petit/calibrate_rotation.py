# -*- coding: utf-8 -*-
'''
Created on 14 mai 2012
'''

from missions.mission import Mission

class CalibrateRotationMission(Mission):
    def __init__(self, robot, can, ui):
        super(self.__class__,self).__init__(robot, can, ui)
        self.rots = 0
        
    def process_event(self, event):
        if self.state == 0:
            if event.name == "start":
                self.state += 1
                self.can.send("asserv rot 9000")
                
        if self.state == 1:
            if event.name == "asserv" and event.type == "done":
                if self.rots < 7:
                    self.rots +=1
                    self.can.send("asserv rot 9000")
                else:
                    self.state += 1
                
            