# -*- coding: utf-8 -*-
'''
Created on 1 mai 2012
'''

from mathutils.types import Segment, Vertex, Vector
from mathutils.geometry import is_segment_intersection


class Bump_sensor:
    def __init__(self, scene, label, position, direction, sensitivity=50):
        '''sensitivity=50 : precision de 5mm'''
        self.robot      = None
        self.state      = "open" # No contact
        self.label      = label
        self.position   = position
        self.direction  = direction
        self.scene      = scene
        self.direction.normalize()
        self.direction *= sensitivity


        
    def init(self):        
        self.sensor     = Segment(Vertex(), self.direction)
        #print(self.sensor.vert1, self.sensor.vert2)
        self.sensor.translate(self.position.x+self.robot.pos.x, 
                              self.position.y+self.robot.pos.y)
#        print(self.sensor)
#        print("init end")
        
    def sense(self):
        self.init()
        for segment in self.scene.plateau.to_segments():
            if is_segment_intersection(segment, self.sensor):
#                print("close!!!")
                return "close"
        return "open"
    
    def run(self):
        new_state = self.sense()
        if new_state != self.state:
            self.state = new_state
            print("bump!!!!!")
            self.robot.msg_can.sender("bump %s %s" % (self.label, new_state))

        