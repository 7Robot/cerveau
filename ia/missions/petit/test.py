# -*- coding: utf-8 -*-
'''
Created on 13 mai 2012
'''

from events.internal import MoveEvent 
from math import cos, sin, pi, copysign

from missions.mission import Mission
from mathutils.types import Vertex
from mathutils.geometry import angle_normalize


class TestMission(Mission):
    def __init__(self, robot, can, ui):
        super(self.__class__,self).__init__(robot, can, ui)
        
    def start(self):
        self.state +=1
        
    def process_event(self, event):
        
        if self.state == 1:
            self.state +=1
            self.move.rotate(self, 9000)
                             
        elif self.state ==2:
            if event.name == "move" and event.type == "done":
                self.state += 1 
                self.move.speed(-10, -10)
        elif self.state == 3:
            if event.name == "bump" and event.state =="close":
                print("Cogne !!!")
                self.state += 1
                self.can.send("asserv stop")
                self.move.stop(self)
        elif self.state == 4:
            if event.name == "move" and event.type == "done":
                self.state += 1
                self.move.forward(self, 1000)
                
                
        elif self.state == 5:
            if event.name == "move" and event.type == "done":
                self.state += 1
                self.move.forward(self, -900)