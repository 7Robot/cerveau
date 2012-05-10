# -*- coding: utf-8 -*-
'''
Created on 30 avr. 2012

Je pense qu'il vaut mieux préfixer les modules par _missions 
car sinon on a des import automatiques de missions qui ont le même nom
'''

# -*-coding:UTF-8 -*

from missions.mission import Mission

class OdoMission(Mission):
    def __init__(self, robot):
        super(self.__class__,self).__init__(robot)
    
    def process_event(self, event):
        if self.state == 0:
            if event.name == "odo":
                if event.type == "pos":
                    self.logger.info("Odo : pos %d %d, theta: %d" % (event.value.x, event.value.y, event.rot))
                    self.robot.pos = event.pos
                    self.robot.theta = event.rot
                elif event.type == "set":
                    self.robot.pos_target = event.pos
                    self.robot.theta_target = event.rot
                    
                    
  




