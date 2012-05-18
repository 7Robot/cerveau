# -*- coding: utf-8 -*-
'''
Created on 15 mai 2012
'''


from missions.mission import Mission
from robots.robot import Robot

class Lingot_MilieuMission(Mission):
    def __init__(self, robot, can, ui):
        super(self.__class__,self).__init__(robot, can, ui)
        
    def process_event(self, e):
        if self.state == 0:
            if e.name == "start":
                self.state += 1
                self.missions["forward"].start(self, -5100)
        
        elif self.state == 1:
            if e.name == "forward" and e.type == "done":
                self.state += 1
                self.missions["rotate"].start(self, -9000)
                
        elif self.state == 2:
            if e.name == "rotate" and e.type == "done":
                self.state += 1
                if Robot.side=="violet":
                    self.missions["forward"].start(self, 10700)
                else:
                    self.missions["forward"].start(self, 10500)
                
        elif self.state == 3:
            if e.name == "forward" and e.type == "done":
                self.state += 1
                self.missions["rotate"].start(self, -4700)
                
        elif self.state == 4:
            if e.name == "rotate" and e.type == "done":
                self.state += 1
                self.missions["forward"].start(self, 7500)
                
        elif self.state == 5:
            if e.name == "forward" and e.type == "done":
                self.state += 1
                self.missions["forward"].start(self, -12500)
                
#        elif self.state == 6:
#            if e.name == "forward" and e.type == "done":
#                self.state += 1
#                self.missions["rotate"].start(self, -13700)
#                
#        elif self.state == 7:
#            if e.name == "rotate" and e.type == "done":
#                self.state += 1
#                self.missions["forward"].start(self, 7800)
#                
#        elif self.state == 8:
#            if e.name == "forward" and e.type == "done":
#                self.state += 1
#                self.missions["rotate"].start(self, -6000)
#                
#        elif self.state == 9:
#            if e.name == "rotate" and e.type == "done":
#                self.state += 1
#                self.missions["speed"].start(20)
                