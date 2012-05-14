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

    def process_event(self, event):
        pass
