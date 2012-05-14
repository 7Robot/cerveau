# -*- coding: utf-8 -*-
'''
Created on 5 mai 2012
'''


from events.event import Event

from missions.mission import Mission
class SpeedRotateMission(Mission):
    def __init__(self, robot, can, ui):
        super(self.__class__,self).__init__(robot, can, ui)
        self.state = "repos"

    # s'orienter dans la direction rot_target
    def start(self, sens, speed):
        if self.state == "repos":
            self.speed = speed
            self.sens = sens
            self.send_event(Event("start", None, self))

    def stop(self, callback):
        if self.state == "run":
            self.callback = callback
            self.state = "stopping"
            self.can.send("asserv stop")

    def process_event(self, event):
        if self.state == "repos" and event.name == "start":
            self.state = "run"
            if self.sens == "droite":
                self.can.send("asserv speed %d 0" %self.speed)
            else:
                self.can.send("asserv speed 0 %d" %self.speed)
                
        elif self.state == "stopping":
            if event.name == "asserv" and event.type == "done":
                self.state = "stopped"
                self.can.send("asserv ticks request")

        elif self.state == "stopped":
            if event.name == "asserv" and event.type == "ticks" and event.cmd == "answer":
                self.state = "repos"
                self.send_event(Event("speedrotate", "done", self.callback, **{"value": event.value}))
                
