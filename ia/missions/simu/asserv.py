# -*- coding: utf-8 -*-
'''
Created on 1 mai 2012
'''

from missions.mission import Mission
class AsservMission(Mission):
    def __init__(self, robot):
        super(self.__class__,self).__init__(robot)
        
    def process_event(self, event):
        if self.state == 0:
            self.state +=1
            self.create_timer(50)
        elif self.state == 1:
            if event.name == "asservt":
                if event.type == "speed":
                    self.robot.asserv_speed(event.value[0], event.curt)
                    self.robot.run()
                    self.create_timer(50)
                elif event.type == "dist":
                    self.robot.asserv_dist(event.value)
                    #self.create_timer(50)
                elif event.type == "rot":
                    self.robot.asserv_rot(event.value)
                    #self.create_timer(50)
                    
                    
            elif event.name == "timerout":
                self.robot.run()
                self.create_timer(50)
                
            
                    
                    
    
    