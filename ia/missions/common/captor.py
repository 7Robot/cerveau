# -*- coding: utf-8 -*-
'''
Created on 5 mai 2012

Liste des tats :
    repos
    forwarding
    pausing
    waiting
    stopping
'''

from events.event import Event
from mathutils.types import Vertex

from math import cos, sin, pi, copysign

from missions.mission import Mission
class CaptorMission(Mission):
    def __init__(self, robot, can, ui):
        super(self.__class__,self).__init__(robot, can, ui)
        # boolean reprsentant la prsence d'obstacle  l'avant et  l'arrire
        # au dmarrage, on considre qu'il n'y a pas d'obstacle
        self._front = False
        self._back = False
        # boolean reprsentant la prsence d'obstacle en face d'un capteur
        self.captors = { 0: False, 1: False, 2: False, 8: False }
        self.dist_y = 0 # customisable
        self.largeur = 0

    def _get_front(self):
        return self._front
    def _set_front(self, front):
        if self._front != front:
            self._front = front
            if front:
                self.logger.info("[front] stop")
                self.send_event(Event("captor", None, [],
                    **{"pos": "front", "state": "stop"}))
            else:
                self.logger.info("[front] start")
                self.send_event(Event("captor", None, [],
                    **{"pos": "front", "state": "start"}))
    front = property(_get_front, _set_front)

    def _get_back(self):
        return self._back
    def _set_back(self, back):
        if self._back != back:
            self._back = back
            if back:
                self.logger.info("[back] stop")
                self.send_event(Event("captor", None, [],
                    **{"pos": "back", "state": "stop"}))
            else:
                self.logger.info("[back] start")
                self.send_event(Event("captor", None, [],
                    **{"pos": "back", "state": "start"}))
    back = property(_get_back, _set_back)

   # def way_is_free(self):
   #     free_way = True
   #     sensors = [] 
   #     if self.remaining > 0:
   #         sensors = [0, 1, 2]
   #     else:
   #         sensors = [8]
   #     for key in sensors:
   #         if not self.free_way[key]:
   #             free_way = False
   #             break
   #     return free_way

    def resume(self, direction):
        if direction == "back":
            self.back = False
        else:
            obstacle = False
            for k in [0, 1, 2]:
                if self.captors[k]:
                    obstacle = True
                    break
            if not obstacle:
                self.front = False


    def process_event(self, event):
        # RANGEFINDER
        if event.name == "rangefinder" \
                and event.type == "value":
            if event.id in [1, 2]:
                if event.value <= self.missions["threshold"].threshold[event.id]:
                    self.captors[event.id] = (event.pos == "under")
                    if not self.front and event.pos == "under":
                        self.front = True
                    elif self.front and event.pos == "over":
                        self.resume("front")
            elif event.id == 8:
                if event.value <= self.missions["threshold"].threshold[event.id]:
                    self.captors[event.id] = (event.pos == "under")
                    if not self.back and event.pos == "under":
                        self.back = True
                    elif self.back and event.pos == "over":
                        self.resume("back")
        elif event.name == "turret" and event.type == "answer":
            hysteresis = 0
            if self.captors[0]:
                hysteresis = 1
            self.captors[0] = False
            for i in range(len(event.angle)):
                event.dist[i] -= 8
                obs_x = event.dist[i]*cos(event.angle[i]/180*pi) # les angles de turret sont en degre
                obs_y = event.dist[i]*sin(event.angle[i]/180*pi)
                if    obs_x < self.robot.turret["right"]+6*hysteresis + self.largeur \
                  and obs_x > -self.robot.turret["left"]-6*hysteresis + self.largeur \
                  and obs_y < (self.robot.turret["front"]+4*hysteresis)*self.missions["threshold"]._sensivity + self.dist_y:
                    if hysteresis == 0:
                        self.logger.info("Laser STOP !")
                        self.front = True
                    self.captors[0] = True
                    break
            if not self.captors[0] and hysteresis == 1:
                self.logger.info("Laser GO !")
                self.resume("front")
