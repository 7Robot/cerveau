# -*- coding: utf-8 -*-
'''
Created on 11 mai 2012
'''


from missions.mission import Mission

class TestMission(Mission):
    def __init__(self, robot, can, ui):
        super(self.__class__,self).__init__(robot, can, ui)
        self.state = "repos"
        
    def process_event(self, event):
        if self.state == "repos":
            if event.name == "ui" and event.type == "test":
                if event.test == "forward":
                    self.missions["move"].forward(self, 1000)