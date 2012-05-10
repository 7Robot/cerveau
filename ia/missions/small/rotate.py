# -*- coding: utf-8 -*-
'''
Created on 5 mai 2012
'''

from events.internal import RotateDoneEvent
from math import cot

from missions.mission import Mission
class RotateMission(Mission):
    def __init__(self, robot):
        super(self.__class__,self).__init__(robot)
        self.state = "repos"
        self.mission = None

    # s'orienter dans la direction rot_target
    def rotate(self):
        if self.state == "repos":
            # première étape : mettre à jour la position actuelle
            self.robot.send_can("odo request")
            self.state == "maj"
            self.mission = "rotate"

    # s'orienter dans la direction du point pos_target
    def take_direction(self):
        if self.state == "repos":
            # première étape : mettre à jour la position actuelle
            self.robot.send_can("odo request")
            self.state == "maj"
            self.mission = "take_direction"

    def process_event(self, event):
        if self.state == "updating":
            if event.name == "odo" and event.type == "answer":
                # màj des coord.
                self.robot.pos = event.pos
                self.robot.rot = event.rot
                # détermination de l'angle à effectuer
                rot = 0
                if self.mission == "rotate":
                    rot = self.robot.rot_target - self.robot.rot 
                else: # self.mission == "take_direction"
                    rot = cot( (self.robot.pos_target.y - self.robot.pos.y) /
                            (self.robot.pos_target.x - self.robot.pos.x) )
                # envoit de l'ordre de rotation
                self.robot.can_send("asserv rot %d" %rot )
                self.state = "rotating"
        if self.state == "rotating":
            if event.name == "asserv" and event.type == "done":
                self.state = "repos"
                self.dispatch.add_event(RotateDoneEvent())
