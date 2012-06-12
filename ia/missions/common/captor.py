# -*- coding: ascii -*-
u'''
Created on 5 mai 2012

Liste des tats :
    repos
    forwarding
    pausing
    waiting
    stopping
'''

from __future__ import division
from events.event import Event
from mathutils.types import Vertex

from math import cos, sin, pi, copysign

from missions.mission import Mission
class CaptorMission(Mission):
    def __init__(self, robot, can, ui):
        super(self.__class__,self).__init__(robot, can, ui)
        # boolean reprsentant la presence d'obstacle  l'avant et  l'arriere
        # au demarrage, on considere qu'il n'y a pas d'obstacle
        self._front = False
        self._back = False
        # boolean representant la presence d'obstacle en face d'un capteur
        self.captors = { 0: False, 1: False, 2: False, 8: False }
        self.dist_y = 0 # customisable
        self.largeur = 0

    def _get_front(self):
        return self._front
    def _set_front(self, front):
        if self._front != front:
            self._front = front
            if front:
                self.logger.info(u"[front] stop")
                self.send_event(Event(u"captor", None, [],
                    **{u"pos": u"front", u"state": u"stop"}))
            else:
                self.logger.info(u"[front] start")
                self.send_event(Event(u"captor", None, [],
                    **{u"pos": u"front", u"state": u"start"}))
    front = property(_get_front, _set_front)

    def _get_back(self):
        return self._back
    def _set_back(self, back):
        if self._back != back:
            self._back = back
            if back:
                self.logger.info(u"[back] stop")
                self.send_event(Event(u"captor", None, [],
                    **{u"pos": u"back", u"state": u"stop"}))
            else:
                self.logger.info(u"[back] start")
                self.send_event(Event(u"captor", None, [],
                    **{u"pos": u"back", u"state": u"start"}))
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
        if direction == u"back":
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
        if event.name == u"rangefinder" \
                and event.type == u"value":
            if event.id in [1, 2]:
                if event.pos == u"over" \
                  and event.value >= self.missions[u"threshold"].threshold[event.id] \
                 or event.pos == u"under" \
                  and event.value <= self.missions[u"threshold"].threshold[event.id]:
                    self.captors[event.id] = (event.pos == u"under")
                    if not self.front and event.pos == u"under":
                        self.front = True
                    elif self.front and event.pos == u"over":
                        self.resume(u"front")
            elif event.id == 8:
                if event.pos == u"over" \
                  and event.value >= self.missions[u"threshold"].threshold[event.id] \
                 or event.pos == u"under" \
                  and event.value <= self.missions[u"threshold"].threshold[event.id]:
                    self.captors[event.id] = (event.pos == u"under")
                    if not self.back and event.pos == u"under":
                        self.back = True
                    elif self.back and event.pos == u"over":
                        self.resume(u"back")
        elif event.name == u"turret" and event.type == u"answer":
            hysteresis = 0
            if self.captors[0]:
                hysteresis = 1
            self.captors[0] = False
            for i in xrange(len(event.angle)):
                event.dist[i] -= 8
                obs_x = event.dist[i]*cos(event.angle[i]/180*pi) # les angles de turret sont en degre
                obs_y = event.dist[i]*sin(event.angle[i]/180*pi)
                if    obs_x < self.robot.turret[u"right"]+6*hysteresis + self.largeur \
                  and obs_x > -self.robot.turret[u"left"]-6*hysteresis + self.largeur \
                  and obs_y < (self.robot.turret[u"front"]+4*hysteresis)*self.missions[u"threshold"]._sensivity + self.dist_y:
                    if hysteresis == 0:
                        self.logger.info(u"Laser STOP !")
                        self.front = True
                    self.captors[0] = True
                    break
            if not self.captors[0] and hysteresis == 1:
                self.logger.info(u"Laser GO !")
                self.resume(u"front")
