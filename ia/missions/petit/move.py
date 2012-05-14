# -*- coding: utf-8 -*-
'''
Created on 30 avr. 2012
'''

from events.internal import MoveEvent 
from math import cos, sin, pi, copysign

from missions.mission import Mission
from mathutils.types import Vertex
from mathutils.geometry import angle_normalize


class MoveMission(Mission):
    def __init__(self, robot, can, ui):
        super(self.__class__,self).__init__(robot, can, ui)
         
        # dernière position connu du robot
        # determiné soit par l'odo, soit par le biais connu du robot
        self._pos = self.robot.pos # position initial
        self._rot = self.robot.rot # orientation initial

        # position demandé du robot
        # initialement, on est à priori là où on veut être
        self._target_pos = self.robot.pos
        self._target_rot = self.robot.rot

        self.odo = None # pas de recalibration en cours
        
        '''
        opération en cours d'execution
        valeurs possibles :
        * None
        * running
        * stopping (demande d'arrêt de speed)
        '''
        self.state = None # pas d'opération en cours

        '''
        mission en cours
        valeur possible :
        * None
        * forward
        * rotate
        * speed
        '''
        self._mission = None # pas de mission en cours

    def _set_pos(self, pos):
        self.logger.debug("[real] pos: %d %d" %(pos.x, pos.y))
        self._pos = pos
    def _get_pos(self):
        return self._pos
    pos = property(_get_pos, _set_pos)

    def _set_target_pos(self, target_pos):
        self.logger.info("[target] pos: %d %d" %(target_pos.x, target_pos.y))
        self._target_pos = target_pos
    def _get_target_pos(self):
        return self._target_pos
    target_pos = property(_get_target_pos, _set_target_pos)

    def _set_rot(self, rot):
        self.logger.debug("[real] rot: %d" %rot)
        self._rot = rot
    def _get_rot(self):
        return self._rot
    rot = property(_get_rot, _set_rot)

    def _set_target_rot(self, target_rot):
        self.logger.info("[target] rot: %d" %target_rot)
        self._target_rot = target_rot
    def _get_target_rot(self):
        return self._target_rot
    target_rot = property(_get_target_rot, _set_target_rot)

    def _set_mission(self, mission):
        self.logger.info("[mission] %s → %s"
                %(self.mission, mission))
        self._mission = mission
    def _get_mission(self):
        return self._mission
    mission = property(_get_mission, _set_mission)

    ### MISSIONS DISPONIBLE ###
    
    # avancer d'une distance donné
    def forward(self, callback, dist):
        '''Le fait de raisonner sur target permet de corriger les imprécisions
        de l'asserv, car target="l'endroit ou l'asserv aurait du nous ammener"'''
        if self.mission == None:
            self.target_pos += Vertex(dist * cos(self.rot/18000*pi), dist * sin(self.rot/18000*pi))
            self.callback = callback
            self.mission = "forward"
            distance = (self.target_pos - self.pos).norm()
            # FIXME: y'a sans doute plus simple
            distance *=  copysign(1, (self.target_pos - self.pos)
                    * Vertex(20*cos(self.rot/18000*pi), 20*sin(self.rot/18000*pi)))
            self.missions["forward"].start(self, distance)

    def rotate(self, callback, angle):
        if self.mission == None:
            self.callback = callback
            self.mission = "rotate"
            self.target_rot += angle
            print("Angle: %d" %angle)
            realangle = angle_normalize(self.target_rot - self.rot)
            print("Pos: %d, Target: %d, Rotate: %d"%(self.rot, self.target_rot,
                realangle))
            if realangle > 17000 and angle < 0:
                realangle = realangle - 36000
            elif realangle < -17000 and angle > 0:
                realangle = realangle + 36000
            print("Rectified angle: %d" %realangle)
            self.missions["rotate"].start(self, realangle)

    def speed(self, left, right, curt = False):
        if self.mission == None:
            self.mission = "speed"
            self.state = "running"
            self.missions["speed"].start(left, right, curt)
            
    def speed_target(self, left, right, curt = False):
        if self.mission == None:
            self.mission = "speed_target"
            self.state = "running"
            self.missions["speed_target"].start(left, right, curt)

    def stop(self, callback):
        if self.mission == "speed":
            self.callback = callback
            self.state = "stopping"
            self.missions["speed"].stop(self)

    ### FIN DES MISSIONS ###

    def process_event(self, event):
        if self.mission == "forward" or self.mission == "rotate" \
                or ((self.mission == "speed" or self.mission == "speed_target") and self.state == "stopping"):
            if event.name == "move" and event.type == "done":
                if self.mission == "speed":
                    self.target_pos += Vertex(event.value * cos(self.rot/18000*pi), event.value * sin(self.rot/18000*pi))
                self.mission = None
                if self.state != None: # c'est pour pas produire de log inutile
                    self.state = None
                self.send_event(MoveEvent("done", [self.callback]))
