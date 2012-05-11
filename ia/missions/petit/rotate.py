# -*- coding: utf-8 -*-
'''
Created on 5 mai 2012
'''

from events.internal import MoveEvent
from mathutils.geometry import angle
from mathutils.geometry import angle_normalize

from missions.mission import Mission
class RotateMission(Mission):
    def __init__(self, robot, can, ui):
        super(self.__class__,self).__init__(robot, can, ui)
        self.state = "repos"

    # s'orienter dans la direction rot_target
    def start(self, order):
        if self.state == "repos":
            self.state = "rotate"
            self.can.send("asserv rot %d" %order)

    def process_event(self, event):
        if self.state == "rotate":
            if event.name == "asserv" and event.type == "done":
                self.state = "repos"
                self.move.process_event(MoveEvent("done"))
