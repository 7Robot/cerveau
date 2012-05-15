# -*- coding: utf-8 -*-
'''
Created on 6 mai 2012
'''

from missions.mission import Mission
from robots.robot import Robot

class UIMission(Mission):
    def __init__(self, robot, can, ui):
        super(self.__class__,self).__init__(robot, can, ui)
        self.state = "repos"
        
    def process_event(self, event):
        if self.state == "repos":
            if event.name == "ui":
                
                if event.type == "calibrate":
                    if "calibrate_rangefinder" in self.missions:
                        self.missions["calibrate_rangefinder"].start(event.id)
                    else:
                        self.logger.error("The mission \'calibrate_rangefinder\' is not loaded")
                    
                elif event.type == "get":
                    if event.mission in self.missions:
                        ans = getattr(self.missions[event.mission], event.attribute)
                        self.ui.send("answer %s" % (ans.__str__()))
                    else:
                        self.ui.send("exception mission %s not found" % (event.mission))
                        
                elif event.type == "init":
                    Robot.side = event.side
                    self.ui.send("answer done")
                    self.missions["positioning"].start()
                
                elif event.type == "message":
                    self.logger.info("UI says: %s" % event.message) 
                        
                        
                elif event.type == "positioning":
                    if "positioning" in self.missions:
                        self.missions["positioning"].start()
                    else:
                        self.logger.error("The mission \'positioning\' is not loaded")
                        
                elif event.type == "set":
                    if event.mission in self.missions:
                        value = event.value 
                        # TODO: double check selon le type de l'attribut
                        try:
                            setattr(self.missions[event.mission], event.attribute, value)
                        except AttributeError as e:
                            self.ui.send("exception %s" % e)
                        else:
                            self.ui.send("answer done")
                    else:
                        self.ui.send("exception mission %s not found" % (event.mission))
                        
                        
                elif event.type == "test":
                    if event.test == "forward":
                        self.missions["move"].forward(self, 1000)
                        self.ui.send("answer done")
                        
                        
      
