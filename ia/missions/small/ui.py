# -*- coding: utf-8 -*-
'''
Created on 6 mai 2012
'''

from missions.mission import Mission
from events.internal import StartEvent

class UIMission(Mission):
    def __init__(self, robot):
        super(self.__class__,self).__init__(robot)
        self.state = "repos"
        
    def process_event(self, event):
        #print("received %s" % event)
        if self.state == "repos":
            if event.name == "ui":
                if event.type == "calibrate":
                    self.robot.send_can("rangefinder %d unmute" % event.id)
                    self.state        = "calibrate rangefinder measurements"
                    self.measurements = []
                    self.id           = event.id
                    self.logger.debug("Start calibration rangefinder %d" % self.id)
                    
                elif event.type == "get":
                    if event.mission in self.missions:
                        getattr(self.missions[event.mission], event.attribute)
                        
                elif event.type == "set":
                    if event.mission in self.missions:
                        value = event.value 
                        # TODO: double check selon le type de l'attribut
                        if event.type == "int":
                            value = int(value)
                        elif  event.type == "float":
                            value = float(value)
                        setattr(self.missions[event.mission], event.attribute, value)

                elif event.type == "positioning":
                    self.missions["positioning"].process_event(StartEvent())
                        
                        
        elif self.state == "calibrate rangefinder measurements":
            # on prend les 16 premières valeurs
            if event.name == "rangefinder" and event.id == self.id \
                and event.type == "value"  and len(self.measurements) < 16:
                self.logger.debug("Calibrating rangefinder %d" % self.id)
                self.measurements.append(event.value)
                if len(self.measurements) >= 16:
                    self.state = "calibrate rangefinder end"
                    
        elif self.state == "calibrate rangefinder end":
            mean = sum(self.measurements)/len(self.measurements)
            self.logger.debug("End calibration rangefinder %d" % self.id)
            self.robot.send_can("rangefinder %d mute" % event.id)
            self.robot.send_can("rangefinder %d mute" % event.id)
            self.robot.send_can("rangefinder %d threshold %d" % (self.id, mean))
            self.state = "repos"
            self.robot.msg_ui.sender("answer calibrate %d done, value is %d" % (self.id, mean))
            
                
