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
        self.state = "mute"

    def broadcast(self, state = "unmute"):
        if state != self.state:
            self.state = state
            self.robot.send_can("odo %s" %state)
    
    def process_event(self, event):
        if self.state == "unmute":
            if event.name == "odo":
                if event.type == "pos":
                    self.robot.pos = event.pos
                    self.robot.theta = event.rot
                elif event.type == "set":
                    self.robot.pos_target = event.pos
                    self.robot.theta_target = event.rot
                    
                    
  




