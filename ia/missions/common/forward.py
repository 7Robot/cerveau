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
class ForwardMission(Mission):
    def __init__(self, robot, can, ui):
        super(self.__class__,self).__init__(robot, can, ui)
        self.state = "repos" # repos | forwarding | pausing | waiting
        self.free_way = True 
        self.abort = False
        
    def start(self, callback, order, abort=False):
        '''C'est moveMission qui va mettre  jour target et nous dire de combien avancer'''
        if self.state == "repos":
            self.abort = abort
#            self.abort = False
            self.order = int(order)
            self.callback = callback
            self.remaining = self.order
            self.state = "forwarding"
            self.can.send("asserv dist %d" % self.remaining)

    def pause(self):
        if self.state == "forwarding":
            self.state = "pausing"
            self.can.send("asserv stop")
        
    def resume(self):
        if self.state == "waiting" and self.free_way:
            self.state = "forwarding"
            self.can.send("asserv dist %d" %self.remaining)
        
    def process_event(self, event):
        if event.name == "captor" \
                and ((event.pos == "front" and self.dist > 0) \
                  or (event.pos == "back"  and self.dist < 0)):
            if event.state == "start":
                self.free_way = True
                if not self.abort:
                    self.resume()
                else:
                    self.state = "repos"
                    self.abort = False
                    self.send_event(Event("forward", "aborted", self.callback))
            else:
                self.free_way = False
                self.pause()

        elif event.name == "asserv" and event.type == "done":
            if self.state == "forwarding" or self.state == "pausing":
                # on a pu aller on voulait aller
                self.state = "repos"
                self.send_event(Event("forward", "done", self.callback))
        elif event.name == "asserv" and event.type == "int_dist":
            if self.state == "pausing":
                self.state = "waiting"
                self.remaining -= event.value
                if not self.abort:
                    self.resume()
                else:
                    self.state = "repos"
                    self.abort = False
                    self.send_event(Event("forward", "aborted", self.callback))
                
