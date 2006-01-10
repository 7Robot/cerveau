# -*- coding: utf-8 -*-
'''
Created on 30 avr. 2012
'''

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

        self.value = {}

    def _set_fonction(self, fonction):
        self.logger.info("[fonction] %s -> %s" %(self._fonction, fonction))
        self._fonction = fonction
    def _get_fonction(self):
        return self._fonction
    fonction = property(_get_fonction, _set_fonction)

    ### FONCTIONS DISPONIBLE ###
    # Elle demmare sur un odo pos pour avoir une valeur a jour

    # avancer de dist
    def forward(self, callback, dist):
        '''Le fait de raisonner sur target permet de corriger les imprcisions
        de l'asserv, car target="l'endroit ou l'asserv aurait du nous ammener"'''
        if self.fonction == None:
            self.fonction = "forward"
            self.callback = callback
            self.value["dist"] = dist
            self.odo.request(self)

    # s'arreter sur la droite x=...
    def reach_x(self, callback, x):
        if self.fonction == None:
            self.fonction = "reach_x"
            self.callback = callback
            self.value["x"] = x
            self.odo.request(self)

    # s'arreter sur la droite y=...
    def reach_y(self, callback, y):
        if self.fonction == None:
            self.fonction = "reach_y"
            self.callback = callback
            self.value["y"] = y
            self.odo.request(self)

    # effectuer une rotation, relative a la position actuelle ou absolue
    def rotate(self, callback, angle, absolute = False):
        if self.fonction == None:
            self.fonction = "rotate"
            self.callback = callback
            self.value["angle"] = angle
            self.value["absolute"] = absolute
            self.odo.request(self)

    def speed(self, speed, curt = False):
        if self.fonction == None:
            self.fonction = "speed"
            self.mission = "speed"
            self.state = "run"
            self.missions["speed"].start(speed, curt)
            
    def stop(self, callback):
        if self.fonction == "speed" and self.state == "run":
            self.callback = callback
            self.state = "stopping"
            self.missions["speed"].stop(self)

    ### FIN DES FONCTIONS ###

    def process_event(self, event):
        if event.name == "odo" and event.type == "answer" and self.mission == None:
            if self.fonction == "forward":
                self.mission = "forward"
                #print("Position actuelle : %s %d" %(event.pos, event.rot))
                #print("Target actuelle : %s %d" %(self.odo.target_pos, self.odo.target_rot))
                deplacement = Vertex(self.value["dist"] * cos(self.odo.target_rot/18000*pi), self.value["dist"] * sin(self.odo.target_rot/18000*pi))
                #print("Distance : %d" %self.value["dist"])
                #print("Vecteur de deplacement : %s" %deplacement)
                self.odo.target_pos += deplacement
                #print("Nouvelle target : %s %d" %(self.odo.target_pos, self.odo.target_rot))
                distance = copysign(deplacement.norm(), self.value["dist"])
                #print("Consigne : %d" %distance)
                self.missions["forward"].start(self, distance)

            elif self.fonction == "reach_x":
                self.mission = "forward"
                #print("Position actuelle : %s %d" %(self.odo.pos, event.rot))
                #print("Consigne: x=%d" %self.value["x"])
                dx = self.value["x"] - event.pos.x
                dtheta = event.rot
                dist = dx/cos(dtheta/18000*pi)
                #print("dx: %d, dtheta: %d, dist: %d" %(dx, dtheta, dist))
                self.odo.target_pos += Vertex(dist * cos(event.rot/18000*pi), dist * sin(event.rot/18000*pi))
                self.missions["forward"].start(self, dist)

            elif self.fonction == "reach_y":
                self.mission = "forward"
                self.logger.info("[reach_y] Position actuelle : %s %d" %(event.pos, event.rot))
                self.logger.info("Consigne: y=%d" %self.value["y"])
                dy = self.value["y"] - event.pos.y
                dtheta = event.rot
                dist = dy/sin(dtheta/18000*pi)
                self.logger.info("dy: %d, dtheta: %d, dist: %d" %(dy, dtheta, dist))
                self.odo.target_pos += Vertex(dist * cos(self.odo.rot/18000*pi), dist * sin(self.odo.rot/18000*pi))
                self.missions["forward"].start(self, dist)

            elif self.fonction == "rotate":
                self.mission = "rotate"
                if self.value["absolute"]:
                    self.odo.target_rot = self.value["angle"]
                else:
                    self.odo.target_rot += self.value["angle"]
                #print("Angle: %d" %self.value["angle"])
                realangle = angle_normalize(self.odo.target_rot - event.rot)
                #print("Pos: %d, Target: %d, Rotate: %d"%(event.rot, self.odo.target_rot, realangle))
                if realangle > 17000 and self.angle < 0:
                    realangle = realangle - 36000
                elif realangle < -17000 and self.angle > 0:
                    realangle = realangle + 36000
                #print("Rectified angle: %d" %realangle)
                self.missions["rotate"].start(self, realangle)

        elif event.name == self.mission and event.type == "done":
            if self.mission == "speed":
                self.odo.target_pos += Vertex(event.value * cos(self.odo.target_rot/18000*pi), event.value * sin(self.odo.target_rot/18000*pi))
                self.state = None
            self.fonction = None
            self.mission = None
            self.send_event(Event("move", "done", [self.callback]))
