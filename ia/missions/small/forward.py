# -*- coding: utf-8 -*-
'''
Created on 5 mai 2012
'''


from missions.mission import Mission
class ForwardMission(Mission):
    def __init__(self, robot):
        super(self.__class__,self).__init__(robot)
        
    def move_forward(self, dist):
        self.dist  = dist
        
        self.state += 1 # sioux : 0 -> 1 ou 2 -> 3
        
    def process_event(self, event):
        if self.state == 1:
            # state = 1 on en en train d'executer une consigne d'asservissement
            if event.name == "sonar":
                # et si on a un obstacle devant
                if event.pos == "under":
                    self.robot.stop()
                    self.state += 1
                
            if event.name == "asserv":
                if event.type == "done":
                    # on a pu aller là où on voulait aller
                    self.state = 0
                    # TODO: notifier le robot
                    
        if self.state == 2:
            if event.name == "asserv":
                if event.type == "int_dist":
                    # le prochain move_forward() va mettre à jour state
                    self.robot.forward(self.dist-self.value)
                
        if self.state == 3:
            # on est arrété
            if event.name ==  "sonar":
                if event.pos == "over":
                    # il n'y a plus rien devant, continuer
                    self.state = 1
            
