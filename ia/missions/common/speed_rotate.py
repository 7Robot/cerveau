# -*- coding: utf-8 -*-
'''
Created on 5 mai 2012
'''

# TODO a passer dans move, nottament pour la gestion de l'odo

from events.event import Event

from missions.mission import Mission
class SpeedRotateMission(Mission):
    def __init__(self, robot, can, ui):
        super(self.__class__,self).__init__(robot, can, ui)
        self.state = "repos"

    # s'orienter dans la direction rot_target
    def start(self, left, right):
        if self.state == "repos":
            self.left = left
            self.right = right
            self.send_event(Event("start", None, self))

    def stop(self, callback):
        if self.state == "run":
            self.callback = callback
            self.state = "stopping"
            self.can.send("asserv stop")

    def process_event(self, event):
        if self.state == "repos" and event.name == "start":
            self.state = "run"
            self.can.send("asserv speed %d %d" %(self.left, self.right))
                
        elif self.state == "stopping":
            if event.name == "asserv" and event.type == "done":
                self.state = "stopped"
                if not self.missions["odo"].brd:
                    self.can.send("odo request")

        elif self.state == "stopped":
            #if event.name == "asserv" and event.tpos "ticks" and event.cmd == "answer":
            if event.name == "odo" and event.type == "pos":
                self.state = "repos"
                self.odo.target_rot = event.rot
                self.send_event(Event("speedrotate", "done", self.callback))