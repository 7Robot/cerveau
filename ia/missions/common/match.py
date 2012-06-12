# -*- coding: utf-8 -*-
u'''
Created on 13 mai 2012
'''

from events.event import Event
import os

from missions.mission import Mission
class MatchMission(Mission):
    def __init__(self, robot, can, ui):
        super(self.__class__,self).__init__(robot, can, ui)
        self.state = u"repos"

    def process_event(self, event):
        if self.state == u"repos":
            if event.name == u"start":
                self.state = u"started"
                self.ui.send(u"start")
                self.create_timer(85000)
        
        elif self.state == u"started" and event.name == u"timer":
                self.state = u"end"
                self.can.send(u"reset")
                self.ui.send(u"stop")
                self.send_event(Event(u"match", u"end"))
                self.create_timer(500)

        elif self.state == u"end" and event.name == u"timer":
                os.execlp(u"killall", u"killall", u"-9", u"python3")
