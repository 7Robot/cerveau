# -*- coding: utf-8 -*-
'''
Created on 5 mai 2012
'''


from events.internal import MoveEvent

from missions.mission import Mission
class SpeedMission(Mission):
    def __init__(self, robot, can, ui):
        super(self.__class__,self).__init__(robot, can, ui)
        self.state = "repos"

    # s'orienter dans la direction rot_target
    def forward(self, speed):
        if self.state == "repos":
            self.speed = speed
            self.state = "forward"
            self.can.send("asserv ticks reset")
            self.can.send("asserv speed %d %d" %(speed, speed))
            
    def rotate(self, sens, speed, callback = None, angle = 0):
        self.speed = speed
        self.state = "rotate"
        if sens == "gauche":
            self.

    def stop(self, callback):
        if self.state == "speed" or self.state == "rotate":
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
                doneEvent = MoveEvent("done", [self.callback])
                doneEvent.value = event.value
                self.send_event(doneEvent)
                
