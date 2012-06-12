# -*- coding: utf-8 -*-
u'''
Created on 16 mai 2012
'''


from events.event import Event
from missions.mission import Mission

class InterComMission(Mission):
    def __init__(self, robot, can, ui):
        super(self.__class__,self).__init__(robot, can, ui)
        
        
        
    def process_event(self, event):
        if self.state == 1:
            if event.name == "intercom":
                pass