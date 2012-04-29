# -*- coding: utf-8 -*-
'''
Created on 30 avr. 2012

Je pense qu'il vaut mieux préfixer les modules par _missions 
car sinon on a des import automatiques de missions qui ont le même nom
'''

# -*-coding:UTF-8 -*

from missions.mission import Mission

class MissionOdo(Mission):

    def __init__(self, robot):
        super(self.__class__,self).__init__("OdoMission", robot)

    def process_event(self, event):
        if self.state == 0:
            if event.name() == "OdoEvent":
                if event.type == "pos":
                    self.robot.set_position(event.value)
                    
  




