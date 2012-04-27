# -*-coding:UTF-8 -*

from missions.mission import Mission

class MissionRecalibration(Mission):

    def __init__(self):
        super(self.__class__,self).__init__(self, "Recalibration")

    def processEvent(self, event):
        if self.state == 0:
            if event.name() == "Start":
                # reculer
                self.state += 1
                                    
        if self.state == 1:
            if event.name() == "BumpEvent":
                if event.state == 1:
                    # set odo = ...
                    self.state += 1
                    
        if self.state == 2:
            if event.name() == "OdoEvent":
                if event.type == "pos":
                    # et si on est bien dans la bonne orientation
                    self.state += 1
                    # reculer
                    
        
        if self.state == 3:
            if event.name() == "BumpEvent":
                if event.state == 1:
                    # set odo = ...
                    self.state += 1
                    # terminé



