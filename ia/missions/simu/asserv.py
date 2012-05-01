# -*- coding: utf-8 -*-
'''
Created on 1 mai 2012
'''

from missions.mission import Mission
class Asserv_listener(Mission):
    def __init__(self, robot):
        super(self.__class__,self).__init__("Asserv", robot)
        
    def process_event(self, event):
        if self.state == 0:
            if event.name() == "AsservEvent":
                if event.type == "speed":
                    self.robot.asserv_speed(event.value[0], event.curt)
                    self.robot.run()
                    self.create_timer(0.05)
                    
            elif event.name() == "Timer_end":
                self.robot.run()
                self.create_timer(1)
                
            
                    
                    
    
    