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
        self.free_way = {"back": True, "front": True} 
        self.abort = False
        
    def start(self, callback, order, autoabort=False):
        '''C'est moveMission qui va mettre  jour target et nous dire de combien avancer'''
        if self.state == "repos":
            self.autoabort = autoabort
            self.order = int(order)
            self.callback = callback
            self.remaining = self.order
            self.state = "run"
            self.missions["threshold"].sensivity(1.5)
            self.can.send("asserv dist %d" % self.remaining)

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
            if ((self.free_way["front"] and self.order > 0) \
                    or (self.free_way["back"] and self.order < 0)):
                self.state = "run" # FIXME mode non-fhomologation
#                self.state = "repos" # FIXME mode homologation
                self.can.send("asserv dist %d" %self.remaining) # FIXME mode non-homologation
        
    def process_event(self, event):
        if event.name == "captor":
            self.free_way[event.pos]  = event.state == "start"
            if self.state != "repos":
                if ((event.pos == "front" and self.order > 0) \
                        or (event.pos == "back" and self.order < 0)):
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
                self.remaining -= event.value
                self.logger.info("Distance remaining: %d/%d"
                        %(self.remaining, self.order))
                self.resume()
            elif self.state == "stopping":
                self.state = "repos"
                self.missions["threshold"].sensivity(1)
                self.send_event(Event("forward", "aborted", self.callback))
                
