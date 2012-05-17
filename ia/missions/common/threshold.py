# -*- coding: utf-8 -*-
'''
Created on 5 mai 2012
'''


from events.event import Event

from missions.mission import Mission
from robots.robot import Robot
class ThresholdMission(Mission):
    def __init__(self, robot, can, ui):
        super(self.__class__,self).__init__(robot, can, ui)
        self.threshold = Robot.rangefinder.copy()
        self._sensivity = 1
    
    def sensivity(self, sensivity):
        self._sensivity = sensivity
        for key in self.threshold:
            if self.threshold[key] != 0:
                self.can.send("rangefinder %d threshold %d"
                        %(key, Robot.rangefinder[key]*sensivity))

    def activate(self, id, status):
        if status:
            self.threshold[id] = Robot.rangefinder[id]*self._sensivity
            self.can.send("rangefinder %d threshold %d" %(id, self.threshold[id]))
        else:
            self.threshold[id] = 0
            self.can.send("rangefinder %d threshold %d" %(id, 0))
