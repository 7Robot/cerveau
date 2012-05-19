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
from robots.robot import Robot

class ForwardMission(Mission):
    def __init__(self, robot, can, ui):
        super(self.__class__,self).__init__(robot, can, ui)
        self.state = "repos" # repos | forwarding | pausing | waiting
        self.abort = False
        
    def start(self, callback, order, autoabort=False):
        '''C'est moveMission qui va mettre  jour target et nous dire de combien avancer'''
        if self.state == "repos":
            self.autoabort = autoabort
            self.order = int(order)
            self.callback = callback
            self.remaining = self.order
            if ((self.captor.front and order > 0 )
                    or (self.captor.back and order < 0)):
                self.state = "paused"
                self.missions["threshold"].sensivity(0.6)
            else:
                self.state = "run"
                self.can.send("asserv dist %d" % self.remaining)
                self.create_timer(200)

    def pause(self):
        if self.state == "run":
            if self.autoabort:
                self.state = "stopping"
            else:
                self.state = "pausing"
            self.can.send("asserv stop")

    def abort(self):
        self.state = "stopping"
        self.can.send("asserv stop")
        
    def resume(self):
        if self.state == "paused":
            if ((not self.captor.front and self.remaining > 0) \
                    or (not self.captor.back and self.remaining < 0)):
                self.state = "run"
                self.can.send("asserv dist %d" %self.remaining)
                self.create_timer(200)
        
    def process_event(self, event):
        if event.name == "timer" and self.state == "run":
            self.missions["threshold"].sensivity(1.3)
        elif event.name == "captor":
            if self.state != "repos":
                if ((event.pos == "front" and self.remaining > 0) \
                        or (event.pos == "back" and self.remaining < 0)):
                    if event.state == "start":
                        self.resume()
                    else:
                        self.pause()

        elif event.name == "asserv" and event.type == "done":
            if self.state != "repos":
                # on a pu aller on voulait aller
                self.state = "repos"
                self.missions["threshold"].sensivity(1)
                self.send_event(Event("forward", "done", self.callback))
        elif event.name == "asserv" and event.type == "int_dist":
            if self.state == "pausing":
                self.state = "paused"
                self.missions["threshold"].sensivity(0.6)
                self.remaining -= event.value
                self.logger.info("Distance remaining: %d/%d"
                        %(self.remaining, self.order))
                self.resume()
            elif self.state == "stopping":
                self.state = "repos"
                self.missions["threshold"].sensivity(1)
                self.remaining -= event.value
                self.send_event(Event("forward", "aborted", self.callback))
                
