# -*- coding: utf-8 -*-
'''
Created on 12 mai 2012
'''

#FIXME  est ce que si l'odo est mute quelqu'un fait des requests périodiques ?

from math import pi

from events.internal import MoveEvent
from mathutils.geometry import angle

from missions.mission import Mission
class Speed_targetMission(Mission):
    '''Ralentit quand on arrive à une certaine distance (20cm)
    de self.move.target'''
    def __init__(self, robot, can, ui):
        super(self.__class__,self).__init__(robot, can, ui)
        self.state = "repos"

    # s'orienter dans la direction rot_target
    def start(self, left, right, curt=False):
        if self.state == "repos":
            self.state = "run"
            self.missions["speed"].start(left, right, curt)

    def stop(self):
        if self.state == "run" or self.state == "slow down":
            self.state = "stopping"
            self.missions["speed"].stop(self)

    def process_event(self, event):
        if self.state == "run":
            if event.name == "odo" and event.type == "pos":
                distance_restante = (self.move.target_pos-event.pos).norm()
                if distance_restante <= 2000:
                    # à 20cm de la target on ralentit
                    self.missions["speed"].change(self.missions["speed"].left/2, self.missions["speed"].right/2)
                    self.state = "slow down"
                    
        if self.state == "stopping":
            if event.name == "asserv" and event.type == "done":
                self.state = "stopped"
                

        if self.state == "stopped":
            if event.name == "asserv" and event.type == "ticks" and event.cmd == "answer":
                self.state = "repos"
