# -*- coding: utf-8 -*-
'''
Created on 5 mai 2012
'''


from events.event import Event

from missions.mission import Mission
class SpeedMission(Mission):
    def __init__(self, robot, can, ui):
        super(self.__class__,self).__init__(robot, can, ui)
        self.state = "repos"

    # s'orienter dans la direction rot_target
    def start(self, speed, curt = False):
        if self.state == "repos":
            self.speed = speed
            self.state = "run"
            self.can.send("asserv ticks reset")
            self.can.send("asserv speed %d %d" %(speed, speed))

    def stop(self, callback):
        if self.state == "run":
            self.callback = callback
            self.state = "stopping"
            self.can.send("asserv stop")

    def process_event(self, event):
        if self.state == "stopping":
            if event.name == "asserv" and event.type == "done":
                self.state = "stopped"
                self.can.send("asserv ticks request")

        if self.state == "stopped":
            if event.name == "asserv" and event.type == "ticks" and event.cmd == "answer":
                self.state = "repos"
                self.send_event(Event("speed", "done", self.callback, **{"value": event.value}))
                
