# -*- coding: utf-8 -*-
u'''
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
        self.state = u"repos" # repos | forwarding | pausing | waiting
        self.abort = False
        
    def start(self, callback, order, autoabort=False):
        u'''C'est moveMission qui va mettre  jour target et nous dire de combien avancer'''
        if self.state == u"repos":
            self.autoabort = autoabort
            self.order = int(order)
            self.callback = callback
            self.remaining = self.order
            if ((self.captor.front and order > 0 )
                    or (self.captor.back and order < 0)):
                self.state = u"paused"
                self.missions[u"threshold"].sensivity(0.6)
            else:
                self.state = u"run"
                self.can.send(u"asserv dist %d" % self.remaining)
                self.create_timer(200)

    def pause(self):
        if self.state == u"run":
            if self.autoabort:
                self.state = u"stopping"
            else:
                self.state = u"pausing"
            self.can.send(u"asserv stop")

    def abort(self):
        self.state = u"stopping"
        self.can.send(u"asserv stop")
        
    def resume(self):
        if self.state == u"paused":
            if ((not self.captor.front and self.remaining > 0) \
                    or (not self.captor.back and self.remaining < 0)):
                self.state = u"run"
                self.can.send(u"asserv dist %d" %self.remaining)
                self.create_timer(200)
        
    def process_event(self, event):
        if event.name == u"timer" and self.state == u"run":
            self.missions[u"threshold"].sensivity(1.3)
        elif event.name == u"captor":
            if self.state != u"repos":
                if ((event.pos == u"front" and self.remaining > 0) \
                        or (event.pos == u"back" and self.remaining < 0)):
                    if event.state == u"start":
                        self.resume()
                    else:
                        self.pause()

        elif event.name == u"asserv" and event.type == u"done":
            if self.state != u"repos":
                # on a pu aller on voulait aller
                self.state = u"repos"
                self.missions[u"threshold"].sensivity(1)
                self.send_event(Event(u"forward", u"done", self.callback))
        elif event.name == u"asserv" and event.type == u"int_dist":
            if self.state == u"pausing":
                self.state = u"paused"
                self.missions[u"threshold"].sensivity(0.6)
                self.remaining -= event.value
                self.logger.info(u"Distance remaining: %d/%d"
                        %(self.remaining, self.order))
                self.resume()
            elif self.state == u"stopping":
                self.state = u"repos"
                self.missions[u"threshold"].sensivity(1)
                self.remaining -= event.value
                self.send_event(Event(u"forward", u"aborted", self.callback))
                
