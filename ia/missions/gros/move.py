# -*- coding: utf-8 -*-
u'''
Created on 30 avr. 2012
'''

from __future__ import division
from events.event import Event 
from math import cos, sin, pi, copysign

from missions.mission import Mission
from mathutils.types import Vertex
from mathutils.geometry import angle_normalize


class MoveMission(Mission):
    def __init__(self, robot, can, ui):
        super(self.__class__,self).__init__(robot, can, ui)
         
        self.mission = None # pas de mission en cours

        self._fonction = None

        self.dist = 0

        self.value = {}

    def _set_fonction(self, fonction):
        self.logger.info(u"[fonction] %s -> %s" %(self._fonction, fonction))
        self._fonction = fonction
    def _get_fonction(self):
        return self._fonction
    fonction = property(_get_fonction, _set_fonction)

    ### FONCTIONS DISPONIBLE ###
    # Elle demmare sur un odo pos pour avoir une valeur a jour

    # avancer de dist
    def forward(self, callback, dist):
        u'''Le fait de raisonner sur target permet de corriger les imprcisions
        de l'asserv, car target="l'endroit ou l'asserv aurait du nous ammener"'''
        if self.fonction == None:
            self.fonction = u"forward"
            self.callback = callback
            self.value[u"dist"] = dist
            self.odo.request(self)

    # s'arreter sur la droite x=...
    def reach_x(self, callback, x):
        if self.fonction == None:
            self.fonction = u"reach_x"
            self.callback = callback
            self.value[u"x"] = x
            self.odo.request(self)

    # s'arreter sur la droite y=...
    def reach_y(self, callback, y):
        if self.fonction == None:
            self.fonction = u"reach_y"
            self.callback = callback
            self.value[u"y"] = y
            self.odo.request(self)

    # effectuer une rotation, relative a la position actuelle ou absolue
    def rotate(self, callback, angle, absolute = False):
        if self.fonction == None:
            self.fonction = u"rotate"
            self.callback = callback
            self.value[u"angle"] = angle
            self.value[u"absolute"] = absolute
            self.odo.request(self)

    def speed(self, speed, curt = False):
        if self.fonction == None:
            self.fonction = u"speed"
            self.mission = u"speed"
            self.state = u"run"
            self.missions[u"speed"].start(speed, curt)
            
    def stop(self, callback):
        if self.fonction == u"speed" and self.state == u"run":
            self.callback = callback
            self.state = u"stopping"
            self.missions[u"speed"].stop(self)

    ### FIN DES FONCTIONS ###

    def process_event(self, event):
        if event.name == u"odo" and event.type == u"answer" and self.mission == None:
            if self.fonction == u"forward":
                self.mission = u"forward"
                #print("Position actuelle : %s %d" %(event.pos, event.rot))
                #print("Target actuelle : %s %d" %(self.odo.target_pos, self.odo.target_rot))
                deplacement = Vertex(self.value[u"dist"] * cos(self.odo.target_rot/18000*pi), self.value[u"dist"] * sin(self.odo.target_rot/18000*pi))
                #print("Distance : %d" %self.value["dist"])
                #print("Vecteur de deplacement : %s" %deplacement)
                self.odo.target_pos += deplacement
                #print("Nouvelle target : %s %d" %(self.odo.target_pos, self.odo.target_rot))
                distance = copysign(deplacement.norm(), self.value[u"dist"])
                #print("Consigne : %d" %distance)
                self.missions[u"forward"].start(self, distance)

            elif self.fonction == u"reach_x":
                self.mission = u"forward"
                self.logger.info(u"[reach_x] Position actuelle : %s %d" %(self.odo.pos, event.rot))
                self.logger.info(u"[reach_x] Consigne: x=%d" %self.value[u"x"])
                dx = self.value[u"x"] - event.pos.x
                dtheta = event.rot
                dist = dx/cos(dtheta/18000*pi)
                self.logger.info(u"[reach_x] dx: %d, dtheta: %d, dist: %d" %(dx, dtheta, dist))
                self.odo.target_pos += Vertex(dist * cos(event.rot/18000*pi), dist * sin(event.rot/18000*pi))
                if (dist > 12500):
                    self.dist = dist / 2
                    dist = self.dist
                    self.fonction == u"reach_x_2"
                self.missions[u"forward"].start(self, dist)

            elif self.fonction == u"reach_y":
                self.mission = u"forward"
                self.logger.info(u"[reach_y] Position actuelle : %s %d" %(event.pos, event.rot))
                self.logger.info(u"[reach_y] Consigne: y=%d" %self.value[u"y"])
                dy = self.value[u"y"] - event.pos.y
                dtheta = event.rot
                dist = dy/sin(dtheta/18000*pi)
                self.logger.info(u"[reach_y] dy: %d, dtheta: %d, dist: %d" %(dy, dtheta, dist))
                self.odo.target_pos += Vertex(dist * cos(self.odo.rot/18000*pi), dist * sin(self.odo.rot/18000*pi))
                self.missions[u"forward"].start(self, dist)

            elif self.fonction == u"rotate":
                self.mission = u"rotate"
                if self.value[u"absolute"]:
                    self.odo.target_rot = self.value[u"angle"]
                else:
                    self.odo.target_rot += self.value[u"angle"]
                #print("Angle: %d" %self.value["angle"])
                realangle = angle_normalize(self.odo.target_rot - event.rot)
                #print("Pos: %d, Target: %d, Rotate: %d"%(event.rot, self.odo.target_rot, realangle))
                if realangle > 17000 and self.angle < 0:
                    realangle = realangle - 36000
                elif realangle < -17000 and self.angle > 0:
                    realangle = realangle + 36000
                #print("Rectified angle: %d" %realangle)
                self.missions[u"rotate"].start(self, realangle)

        elif event.name == self.mission and event.type == u"done":
            if self.fonction == u"reach_x_2" and self.dist != 0:
                self.missions[u"forward"].start(self, dist)
                self.fonction = u"reach_x"
            else:
                if self.mission == u"speed":
                    self.odo.target_pos += Vertex(event.value * cos(self.odo.target_rot/18000*pi), event.value * sin(self.odo.target_rot/18000*pi))
                    self.state = None
                self.fonction = None
                self.mission = None
            self.send_event(Event(u"move", u"done", [self.callback]))
