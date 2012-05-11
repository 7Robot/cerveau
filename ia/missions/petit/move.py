# -*- coding: utf-8 -*-
'''
Created on 30 avr. 2012
'''

from events.internal import MoveEvent 
from math import cos, sin, pi, copysign

from missions.mission import Mission
from mathutils.types import Vertex


class MoveMission(Mission):
    def __init__(self, robot, can, ui):
        super(self.__class__,self).__init__(robot, can, ui)
         
        # dernière position connu du robot
        # determiné soit par l'odo, soit par le biais connu du robot
        self.pos = self.robot.pos # position initial
        self.rot = self.robot.rot # orientation initial

        # position demandé du robot
        # initialement, on est à priori là où on veut être
        self.target_pos = self.robot.pos
        self.target_rot = self.robot.rot
        
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

    def _set_mission(self, mission):
        self.logger.info("[%s] (mission)%s → (mission)%s"
                %(self.name, self.mission, mission))
        self._mission = mission

    def _get_mission(self):
        return self._mission

    mission = property(_get_mission, _set_mission)

    ### MISSIONS DISPONIBLE ###
    
    # avancer d'une distance donné
    def forward(self, callback, dist):
        if self.mission == None:
            self.callback = callback
            self.mission = "forward"
            distance = (self.target_pos - self.pos).norm()
            distance *=  copysign(1, (self.robot.pos_target - self.robot.pos)
                    * Vertex(20*cos(self.robot.theta/18000*pi), 20*sin(self.robot.theta/18000*pi)))
            self.missions["forward"].start(distance)

    def rotate(self, callback, angle):
        if self.mission == None:
            self.callback = callback
            self.mission = "rotate"
            angle = angle_normalize(angle)
            self.missions["rotate"].start(angle)

    def speed(self, left, right, curt = False):
        if self.mission == None:
            self.mission = "speed"
            self.state = "running"
            self.missions["speed"].start(left, right, curt)

    def stop(self, callback):
        if self.mission == "speed":
            self.callback = callback
            self.state = "stopping"
            self.missions["speed"].stop()

    ### FIN DES MISSIONS ###

    def process_event(self, event):
        # events gérés quelque soit l'état
        if event.name == "odo":
            if event.type == "pos":
                # màj de la position actuelle
                self.pos = event.pos
                self.rot = event.rot

        # events gérés suivant l'état
        if self.mission == "forward" or self.mission == "rotate" \
                or (self.mission == "speed" and self.state == "stopping"):
            if event.name == "move" and event.type == "done":
                self.callback.process_event(MoveEvent("done"))
                self.mission = None
                self.state = None
