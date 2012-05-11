# -*- coding: utf-8 -*-
'''
Created on 5 mai 2012

Liste des états :
    repos
    forwarding
    pausing
    waiting
    stopping
'''

from events.internal import MoveEvent
from mathutils.types import Vertex

from math import cos, sin, pi, copysign

from missions.mission import Mission
class ForwardMission(Mission):
    def __init__(self, robot, can, ui):
        super(self.__class__,self).__init__(robot, can, ui)
        self.state = "repos"
        self.free_way = { 0: True, 1: True, 2: True, 8: True }

    def start(self, order):
        '''C'est moveMission qui va mettre à jour target et nous dire de combien avancer'''
        if self.state == "repos":
            self.order = int(order)
            self.remaining = self.order
            self.state = "forwarding"
            self.can.send("asserv dist %d" % self.remaining)

    def stop(self):
        if self.state == "forwarding":
            self.state = "stopping"
            self.can.send("asserv stop")
        elif self.state == "pausing":
            self.state = "stopping"
        else:
            self.state = "repos"
            event = MoveEvent("int")
            event.value = self.order - self.remaining
            self.missions["move"].process_event(event)

    def pause(self):
        if self.state == "forwarding":
            self.state = "pausing"
            self.can.send("asserv stop")
        
    def resume(self):
        if self.state == "waiting":
            if self.way_is_free():
                self.state = "forwarding"
                self.can.send("asserv dist %d" %self.remaining)
        
    def process_event(self, event):
        # events des capteurs
        if event.name == "rangefinder" \
                and event.id in [1,2,8] \
                and event.type == "answer":
            self.free_way[event.id] = (event.pos == "over")
            if self.state == "forwarding" and event.pos == "under":
                self.pause()
            if self.state == "waiting" and event.pos == "over":
                self.resume()
        elif event.name == "turret" and event.type == "answer":
            hysteresis = 0
            if not self.free_way[0]:
                hysteresis = 1
            self.free_way[0] = True
            for i in range(len(event.angle)):
                event.dist[i] -= 8
                obs_x = event.dist[i]*cos(event.angle[i]/180*pi) # les angles de turret sont en degré
                obs_y = event.dist[i]*sin(event.angle[i]/180*pi)
                if    obs_x < self.robot.turret["right"]+8*hysteresis \
                  and obs_x > -self.robot.turret["left"]-8*hysteresis \
                  and obs_y < self.robot.turret["front"]+4*hysteresis:
                    if hysteresis == 0:
                        self.logger.info("Laser STOP !")
                        self.pause()
                    self.free_way[0] = False
                    break
            if self.free_way[0] and hysteresis == 1:
                self.resume()
                self.logger.info("Laser GO !")

        # events triés suivant l'état
        if self.state == "forwarding":
            if event.name == "asserv" and event.type == "done":
                # on a pu aller là où on voulait aller
                self.state = "repos"
                self.dispatch.add_event(MoveEvent("done"))
        elif self.state == "pausing":
            if event.name == "asserv" and event.type == "int_dist":
                self.state = "waiting"
                self.remaining -= event.value
                self.resume()

    def way_is_free(self):
        free_way = True
        sensors = [] 
        if self.remaining > 0:
            sensors = [0, 1, 2]
        else:
            sensors = [8]
        for key in sensors:
            if not self.free_way[key]:
                free_way = False
                break
        return free_way
        

