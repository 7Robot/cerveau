# -*- coding: utf-8 -*-
'''
Created on 6 mai 2012
'''

from missions.mission import Mission
class UIMission(Mission):
    def __init__(self, robot):
        super(self.__class__,self).__init__(robot)
        
    def process_event(self, event):
        if event.name == "ui":
            if event.type == "rangefinder_calibrate":
                pass
                # unmute + moyenne + set thresold + mute
                
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