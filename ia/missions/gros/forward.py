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
        self.aborting = False
        self.callback = None
        
    def abort(self, callback):
        '''Interrompre la mission en cours'''
        self.aborting = True
        self.callback = callback
        if self.state == "waiting":
            self.state = "repos"
            self.send_event(Event("forward", "aborted", self.callback))
        else:
	        self.pause(callback)

    def start(self, callback, order):
        '''C'est moveMission qui va mettre  jour target et nous dire de combien avancer'''
        if self.state == "repos":
            self.abort = False
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
        if event.name == "captor" and event.pos == "front":
            if event.state == "start":
                self.free_way = True
                self.resume()
            else:
                self.free_way = False
                self.pause()

        # events tris suivant l'tat
        if self.state == "forwarding":
            if event.name == "asserv" and event.type == "done":
                # on a pu aller l o on voulait aller
                self.state = "repos"
                self.send_event(Event("forward", "done", self.callback))
        elif self.state == "pausing":
            if event.name == "asserv" and event.type == "int_dist":
                self.state = "waiting"
                self.remaining -= event.value
                if not self.aborting:
                    self.resume()
                else:
                    self.send_event(Event("forward", "aborted", self.callback))
                