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
        self.free_way = True 
        self.aborting = False
        self.callback = None
        
    def abort(self, callback):
        '''Interromp la mission en cours'''
        self.aborting = True
        self.callback = callback
        self.pause(callback)
            
        

    def start(self, callback, order):
        '''C'est moveMission qui va mettre à jour target et nous dire de combien avancer'''
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

        # events triés suivant l'état
        if self.state == "forwarding":
            if event.name == "asserv" and event.type == "done":
                # on a pu aller là où on voulait aller
                self.state = "repos"
                self.send_event(MoveEvent("done", self.callback))
        elif self.state == "pausing":
            if event.name == "asserv" and event.type == "int_dist":
                self.state = "waiting"
                self.remaining -= event.value
                if not self.aborting:
                    self.resume()
                else:
                    self.send_event(MoveEvent("aborted", self.callback))
                
