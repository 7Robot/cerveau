# -*- coding: utf-8 -*-
u'''
Created on 15 mai 2012
'''

from missions.mission import Mission
from robots.robot import Robot

class Rase_totemMission(Mission):
    def __init__(self, robot, can, ui):
        super(self.__class__,self).__init__(robot, can, ui)
        
    def process_event(self, e):
        if self.state == 0:
            if e.name == "start":
                self.state += 0.5
                self.create_timer(1000)
                self.missions["speed"].start(-60)
        
        elif self.state == 0.5:
            if e.name == "timer":
                self.state += 0.5
                self.create_timer(5000)
                self.missions["speed"].start(-30)
                
        elif self.state == 1:
            if (e.name == "bump" and e.state == "close"  \
                    and e.pos == "back") or e.name == "timer":
                self.state += 1
                self.missions["speed"].stop(self)
                
        elif self.state == 2:
            if e.name == "speed" and e.type == "done":
                self.state += 1
                self.create_timer(5000)
                
        elif self.state == 3:
            if e.name == "timer":
                self.state += 1
                self.missions["forward"].start(self, 800)
                
        elif self.state == 4:
            if e.name == "forward" and e.type == "done":
                self.state += 1
                self.missions["rotate"].start(self, -9000)
                
        elif self.state == 5:
            if e.name == "rotate" and e.type == "done":
                self.state += 1
                self.missions["forward"].start(self, 8700)
                
        elif self.state == 6:
            if e.name == "forward" and e.type == "done":
                self.state += 1
                self.missions["rotate"].start(self, -3300)
                
        elif self.state == 7:
            if e.name == "rotate" and e.type == "done":
                self.state += 1
                self.missions["forward"].start(self, 8000)
                
        elif self.state == 8:
            if e.name == "forward" and e.type == "done":
                self.state += 1
                self.missions["forward"].start(self, -8000)