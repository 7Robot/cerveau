# -*- coding: utf-8 -*-
'''
Created on 13 mai 2012
'''

from missions.mission import Mission

class MatchMission(Mission):
    def __init__(self, robot, can, ui):
        super(self.__class__,self).__init__(robot, can, ui)
        self.state = "repos"

    def process_event(self, event):
        if self.state == "repos":
            if event.name == "start": #FIXME : personne l\'envoie
                self.state = "match started"
                self.ui.send("start")
                self.create_timer(90000)
        if self.state == "match started":
            if event.name == "timer":
                self.state = "fin match"
                self.ui.send("stop")
