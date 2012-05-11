## -*- coding: utf-8 -*-
#'''
#Created on 5 mai 2012
#'''
#
#from math import pi
#
#from events.internal import RotateDoneEvent
#from mathutils.geometry import angle
#
#from missions.mission import Mission
#class RotateMission(Mission):
#    def __init__(self, robot, can, ui):
#        super(self.__class__,self).__init__(robot, can, ui)
#        self.state = "repos"
#        self.mission = None
#
#    def disable(self):
#        self.state = "repos"
#
#    # s'orienter dans la direction rot_target
#    def rotate(self):
#        if self.state == "repos":
#            # première étape : mettre à jour la position actuelle
#            self.can.send("odo request")
#            self.state = "updating"
#            self.mission = "rotate"
#
#    # s'orienter dans la direction du point pos_target
#    def take_direction(self):
#        if self.state == "repos":
#            # première étape : mettre à jour la position actuelle
#            self.can.send("odo request")
#            self.state = "updating"
#            self.mission = "take_direction"
#
#    def process_event(self, event):
#        if self.state == "updating":
#            if event.name == "odo" and event.type == "answer":
#                # màj des coord.
#                self.mission["move"].pos = event.pos
#                self.mission["move"].rot = event.rot
#                # détermination de l'angle à effectuer
#                rot = 0
#                if self.mission == "rotate":
#                    rot = self.robot.normal_angle(self.robot.rot_target - self.robot.rot) # FIXME normal angle
#                else: # self.mission == "take_direction"
#                    #rot = self.robot.normal_angle( atan2( (self.robot.pos_target.y - self.robot.pos.y) /
#                    #        (self.robot.pos_target.x - self.robot.pos.x) ) * 18000 / pi )
#                    rot = angle(self.robot.pos_target, self.robot.pos) * 18000 / pi
#                # envoit de l'ordre de rotation
#                self.can.send("asserv rot %d" %rot )
#                self.state = "rotating"
#        if self.state == "rotating":
#            if event.name == "asserv" and event.type == "done":
#                self.state = "repos"
#                self.dispatch.add_event(RotateDoneEvent())