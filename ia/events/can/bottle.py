# -*- coding: utf-8 -*-
'''
Created on 12 mai 2012
'''

from missions.mission import Mission

class BottleMission(Mission):
    def __init__(self, robot, can, ui):
        super(self.__class__,self).__init__(robot, can, ui)
        self.state = "repos"
        
    def process_event(self, event):
        pass
        # Cette mission n'est executable que si on est bien placé :
        
        # utiliser move.speed_target