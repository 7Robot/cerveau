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
         
        # dernire position connu du robot
        # determin soit par l'odo, soit par le biais connu du robot
        #self._pos = self.robot.pos # position initial
        #self._rot = self.robot.rot # orientation initial

        # position demand du robot
        # initialement, on est  priori l o on veut tre
        #self._target_pos = self.robot.pos
        #self._target_rot = self.robot.rot

        #self.odo = None # pas de recalibration en cours
        '''
        mission en cours
        valeur possible :
        * None
        * forward
        * rotate
        * speed
        '''
        self.mission = None # pas de mission en cours

        self._fonction = None

        self.value = {}

    #def _set_pos(self, pos):
    #    self.logger.debug("[real] pos: %d %d" %(pos.x, pos.y))
    #    self._pos = pos
    #def _get_pos(self):
    #    return self._pos
    #pos = property(_get_pos, _set_pos)

    #def _set_target_pos(self, target_pos):
    #    self.logger.debug("[target] pos: %d %d" %(target_pos.x, target_pos.y))
    #    self._target_pos = target_pos
    #def _get_target_pos(self):
    #    return self._target_pos
    #target_pos = property(_get_target_pos, _set_target_pos)

    #def _set_rot(self, rot):
    #    self.logger.debug("[real] rot: %d" %rot)
    #    self._rot = rot
    #def _get_rot(self):
    #    return self._rot
    #rot = property(_get_rot, _set_rot)

    #def _set_target_rot(self, target_rot):
    #    self.logger.debug("[target] rot: %d" %target_rot)
    #    self._target_rot = target_rot
    #def _get_target_rot(self):
    #    return self._target_rot
    #target_rot = property(_get_target_rot, _set_target_rot)

    #def _set_mission(self, fonction):
    #    self.logger.info("[mission] %s -> %s"
    #            %(self.mission, mission))
    #    self._mission = mission
    #def _get_mission(self):
    #    return self._mission
    #mission = property(_get_mission, _set_mission)

    def _set_fonction(self, fonction):
        self.logger.info("[fonction] %s -> %s" %(self._fonction, fonction))
        self._fonction = fonction
    def _get_fonction(self):
        return self._fonction
    fonction = property(_get_fonction, _set_fonction)

    ### FONCTIONS DISPONIBLE ###
    # Elle demmare sur un odo pos pour avoir une valeur a jour

    def run(self):
        if not self.odo.brd:
            self.can.send("odo request")
    
    # avancer de dist
    def forward(self, callback, dist):
        '''Le fait de raisonner sur target permet de corriger les imprcisions
        de l'asserv, car target="l'endroit ou l'asserv aurait du nous ammener"'''
        if self.fonction == None:
            self.fonction = "forward"
            self.callback = callback
            self.value["dist"] = dist
            self.run()

    # s'arreter sur la droite x=...
    def reach_x(self, callback, x):
        if self.fonction == None:
            self.fonction = "reach_x"
            self.callback = callback
            self.value["x"] = x
            self.run()

    # s'arreter sur la droite y=...
    def reach_y(self, callback, y):
        if self.fonction == None:
            self.fonction = "reach_y"
            self.callback = callback
            self.value["y"] = y
            self.run()

    # effectuer une rotation, relative a la position actuelle ou absolue
    def rotate(self, callback, angle, absolute = False):
        if self.fonction == None:
            self.fonction = "rotate"
            self.callback = callback
            self.value["angle"] = angle
            self.value["absolute"] = absolute
            self.run()

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
        if event.name == "odo" and event.type == "pos" and self.mission == None:
            self.odo.pos = event.pos
            self.odo.rot = event.rot
            if self.fonction == "forward":
                self.mission = "forward"
                #print("Position actuelle : %s %d" %(self.odo.pos, self.odo.rot))
                #print("Target actuelle : %s %d" %(self.odo.target_pos, self.odo.target_rot))
                deplacement = Vertex(self.value["dist"] * cos(self.odo.target_rot/18000*pi), self.value["dist"] * sin(self.odo.target_rot/18000*pi))
                #print("Distance : %d" %dist)
                #print("Vecteur de deplacement : %s" %deplacement)
                self.odo.target_pos += deplacement
                #print("Nouvelle target : %s %d" %(self.odo.target_pos, self.odo.target_rot))
                distance = copysign(deplacement.norm(), self.value["dist"])
                #distance *=  copysign(1, (self.odo.target_pos - self.odo.pos) # FIXME moche !
                #        * Vertex(20*cos(self.odo.rot/18000*pi), 20*sin(self.odo.rot/18000*pi)))
                #print("Consigne : %d" %distance)
                self.missions["forward"].start(self, distance)

            elif self.fonction == "reach_x":
                self.mission = "forward"
                #print("Position actuelle : %s %d" %(self.odo.pos, self.odo.rot))
                #print("Consigne: x=%d" %self.x)
                dx = self.value["x"] - self.odo.pos.x
                dtheta = self.odo.rot
                dist = dx/cos(dtheta/18000*pi)
                #print("dx: %d, dtheta: %d, dist: %d" %(dx, dtheta, dist))
                self.odo.target_pos += Vertex(dist * cos(self.odo.rot/18000*pi), dist * sin(self.odo.rot/18000*pi))
                self.missions["forward"].start(self, dist)

            elif self.fonction == "reach_y":
                self.mission = "forward"
                dy = self.value["y"] - self.odo.pos.y
                dtheta = self.odo.rot
                dist = dy/sin(dtheta/18000*pi)
                #print("dy: %d, dtheta: %d, dist: %d" %(dy, dtheta, dist))
                self.odo.target_pos += Vertex(dist * cos(self.odo.rot/18000*pi), dist * sin(self.odo.rot/18000*pi))
                self.missions["forward"].start(self, dist)

            elif self.fonction == "rotate":
                self.mission = "rotate"
                if self.value["absolute"]:
                    self.odo.target_rot = self.value["angle"]
                else:
                    self.odo.target_rot += self.value["angle"]
                #print("Angle: %d" %angle)
                realangle = angle_normalize(self.odo.target_rot - self.odo.rot)
                #print("Pos: %d, Target: %d, Rotate: %d"%(self.rot, self.target_rot,
                #    realangle))
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
