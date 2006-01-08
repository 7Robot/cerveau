# -*- coding: utf-8 -*-
'''
Created on 5 mai 2012
'''


from missions.mission import Mission
class ForwardMission(Mission):
    def __init__(self, robot):
        super(self.__class__,self).__init__(robot)
        
    def process_event(self, event):
            if self.state == 1:
                # state = 1 on en en train d'executer une consigne d'asservissement
                # don on fait des sonars requests périodiquement
                if event.name == "sonar":
                    # est si on a un obstacle devant
                    # if range under
                    self.robot.stop()
                    self.state = 2
                    
                if event.name == "asserv":
                    if event.type == "done":
                        # on a pu aller là où on voulait aller
                        self.state = 0
                        # notifier le robot
                    
            if self.state == 2:
                # state = 2 : on est arrété
                if event.name ==  "sonar":
                    # il n'y a plus rien devant continuer
                    pass
                
    