# -*- coding: utf-8 -*-
'''
Created on 8 mai 2012
'''

from missions.mission import Mission
class TestForwardMission(Mission):
    def __init__(self, robot):
        super(self.__class__,self).__init__(robot)
        
    def process_event(self, e):
        print("see event %s", e)
        if e.name == "bump" and e.state == "close":
            self.logger.debug("On avance !!!!")
            self.robot.forward(15000)
