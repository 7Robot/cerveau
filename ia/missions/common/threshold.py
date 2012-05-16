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
        self.threshold = Robot.threshold
        self.sensivity = 1
    
    def sensivity(self, sensivity):
        print("set sensivity %d" %sensivity)
        self.sensivity = sensivity
        for key in self.threshold:
            if self.threshold[key] != 0:
                self.can.send("rangefinder %d threshold %d"
                        %(Robot.threshold[key]*sensivity))
            else:
                print("rangefinder %d ignored" %key)

    def activate(self, id, status):
        if status:
            print("activate rangefinder %d" %id)
            self.threshold[id] = Robot.threshold[id]*self.sensivity))
            self.can.send("rangefinder %d threshold %d" %(id, self.threshold[id]))
        else:
            print("deactivate rangefinder %d" %id)
            self.threshold[id] = 0
            self.can.send("rangefinder %d threshold %d" %(id, 0))
