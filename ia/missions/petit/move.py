# -*- coding: utf-8 -*-
'''
Created on 30 avr. 2012
'''

from events.internal import MoveDoneEvent 
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
        * stopping
        '''
        self.state = None # pas d'opération en cours

        '''
        mission en cours
        valeur possible :
        * None
        * forward
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
        self.callback = callback
        self.mission = "forward"
        self.dist = dist
        self.stop()

    def rotate(self, callback, angle):
        self.callback = callback
        self.mission = "rotate"
        self.angle = angle

    ### FIN DES MISSIONS ###

    # stopper la mission en cours
    def stop(self):
        if self.mission == None:
            self.process_event(MoveDoneEvent())
        elif self.mission == "forward":
            self.state = "stopping"
            self.missions["forward"].stop()

    def process_event(self, event):
        # events gérés quelque soit l'état
        if event.name == "odo":
            if event.type == "pos":
                # màj de la position actuelle
                self.pos = event.pos
                self.rot = event.rot

        # events gérés suivant la mission en cours
        if self.mission == "forward": # mission d'avancement
            if event.name == "movedone": # la mission précédente est terminé
                self.target_pos = self.pos \
                        + Vertex(self.dist * cos(self.rot/18000*pi),
                                self.dist * sin(self.rot/18000*pi))
                self.state = "forwarding"
                self.missions["forward"].start()
            elif event.name == "forwarddone": # arrêt
                if self.state == "forwarding":
                    # l'avancement est terminé
                    self.state = None
                    self.mission = None
                    self.callback.process_event(MoveDoneEvent())
                elif self.state == "stopping":
                    # l'arrêt de l'oppération est terminé
                    self.process_event(MoveDoneEvent())
