# -*- coding: utf-8 -*-
'''
Created on 13 mai 2012
'''
from math import cos

from missions.mission import Mission

class ForwardDistMission(Mission):
    def __init__(self, robot, can, ui):
        super(self.__class__,self).__init__(robot, can, ui)
        self.state = "repos"
        
    def move_until_x(self, value):
        '''Précondition : on avance selon l'axe des X'''
        dist   = abs(value - self.move.pos.x)
        dtheta = abs(self.rot)
        dist   = dist/cos(dtheta)
        self.move.forward(dist)
        
        
        
    
    