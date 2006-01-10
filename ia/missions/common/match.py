# -*- coding: utf-8 -*-
'''
Created on 13 mai 2012
'''

from events.event import Event
import os

from missions.mission import Mission
class MatchMission(Mission):
    def __init__(self, robot, can, ui):
        super(self.__class__,self).__init__(robot, can, ui)
        self.state = "repos"

    def process_event(self, event):
        if self.state == "repos":
            if event.name == "start":
                self.state = "started"
                self.ui.send("start")
                self.create_timer(89000)
        
        elif self.state == "started" and event.name == "timer":
                self.state = "end"
                self.can.send("asserv stop")
                self.can.send("ax 1 torque set 0")
                self.can.send("asserv off")
                self.can.send("ax 2 torque set 0")
                self.ui.send("stop")
                self.send_event(Event("match", "end"))
                self.create_timer(1000)

        elif self.state == "end" and event.name == "timer":
                os.execlp("killall", "killall", "-9", "python3")
