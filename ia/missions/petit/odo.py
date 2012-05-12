# -*- coding: utf-8 -*-
'''
Created on 30 avr. 2012
'''

from events.internal import MoveEvent 
from math import cos, sin, pi, copysign

from missions.mission import Mission
from mathutils.types import Vertex
from mathutils.geometry import angle_normalize
from events.internal import OdoEvent


class OdoMission(Mission):
    def __init__(self, robot, can, ui):
        super(self.__class__,self).__init__(robot, can, ui)
         
        self.state = None # pas de recalibration en cour
        self.brd = False # par defaut, pas de broadcast de l'odo

    def broadcast(self, state = True):
        if state != self.brd:
            self.brd = state
            if state:
                self.can.send("odo unmute")
            else:
                self.can.send("odo mute")

    def set(self, callback, **value):
        self.state = "calibrating"
        self.callback = callback
        self.value = value
        if not self.broadcast:
            self.can.send("odo request")

    def process_event(self, event):
        # events gérés quelque soit l'état
        if event.name == "odo" and event.type == "pos":
            if self.state == "calibrating":
                self.state = None

                for axe in self.value:
                    if axe == "x":
                        event.pos.x = self.value["x"]
                    elif axe == "y": 
                        event.pos.y = self.value["y"]
                    elif axe == "rot":
                        event.rot = self.value["rot"]

                self.move.pos = event.pos
                self.move.rot = event.rot
                self.can.send("odo set %d %d %d"
                        % (event.pos.x/10, event.pos.y/10, event.rot))

                self.callback.process_event(OdoEvent("done"))
            else:
                self.move.pos = event.pos
                self.move.rot = event.rot
                self.logger.debug("Position : %d %d, Direction : %d"
                        %(self.move.pos.x, self.move.pos.y, self.move.rot))

