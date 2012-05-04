# -*- coding: utf-8 -*-
'''
Created on 4 mai 2012

'''


from missions.mission import Mission


class AsservMission(Mission):
    def __init__(self, robot):
        super(self.__class__,self).__init__(robot)
    
    def process_event(self, event):
        if self.state == 0:
            if event.name == "asserv":
                if event.type == "done":
                    self.robot.pos_target = None
                elif event.type == "int_dist":
                    # mise à jour des coordonnées inutile car l'odo nous la donne ?
                    # prévenir le robot/le mission manager d'une interruption
                    pass
                    
                    
  




