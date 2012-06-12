# -*- coding: utf-8 -*-
u'''
Created on 5 mai 2012
'''

from events.event import Event
from mathutils.geometry import angle
from mathutils.geometry import angle_normalize

from missions.mission import Mission
class RotateMission(Mission):
    def __init__(self, robot, can, ui):
        super(self.__class__,self).__init__(robot, can, ui)
        self.state = u"repos"

    # s'orienter dans la direction rot_target
    def start(self, callback, order):
        if self.state == u"repos":
            self.order = order
            self.callback = callback
            self.send_event(Event(u"start", None, self))

    def process_event(self, event):
        if self.state == u"repos" and event.name == u"start":
            self.state = u"rotate"
            self.can.send(u"asserv rot %d" %self.order)
            
        elif self.state == u"rotate":
            if event.name == u"asserv" and event.type == u"done":
                self.state = u"repos"
                self.send_event(Event(u"rotate", u"done", self.callback))
