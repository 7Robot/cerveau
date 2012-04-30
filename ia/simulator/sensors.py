# -*- coding: utf-8 -*-
'''
Created on 1 mai 2012
'''

from mathutils.types import Segment, Vertex, Vector
from mathutils.geometry import is_segment_intersection

class Bump_sensor:
    def __init__(self, label, position, direction, real_robot, scene, sensitivity=50):
        '''sensitivity=50 : precision de 5mm'''
        self.state      = "open" # No contact
        self.label      = label
        self.position   = position
        self.direction  = direction
        self.real_robot = real_robot
        self.scene      = scene
        self.direction.normalize()
        self.direction *= sensitivity
        self.generate_sensor()
        
    def generate_sensor(self):        
        self.sensor     = Segment(Vertex(), self.direction)
        self.sensor.translate(self.position.x+self.real_robot.x, self.position.y+self.real_robot.y)
        
    def sense(self):
        for segment in self.scene.to_segements():
            if is_segment_intersection(segment, self.sensor):
                return "close"
        return "open"
    
    def generate_event(self):
        new_state = self.sense()
        if new_state != self.state:
            self.state = new_state
            return "bump %s %s" % (self.label, new_state)