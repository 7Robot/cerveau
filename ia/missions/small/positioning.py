# -*-coding:UTF-8 -*

from missions.mission import Mission

class PositioningMission(Mission):

    def process_event(self, event):
        if self.state == 0:
            if event.name == "start":
                self.robot.rotate(-900);
                self.state += 1

        if self.state == 1:
            if event.name == "asserv":
                if event.type == "done_rot":
                    self.robot.asserv(20, 20)
                    self.state += 1
                                    
        if self.state == 2:
            if event.name == "bump":
                if event.state == "close":
                    self.robot.stop();
                    missions.Mission.create_time(700)
                    self.state += 1
                    
        if self.state == 2:
            if event.name == "odo":
                if event.type == "pos":
                    # et si on est bien dans la bonne orientation
                    self.state += 1
                    self.robot.forward(3000)
        
        if self.state == 3:
            if event.name == "asserv":
                if event.type == "done_dist":
                    self.state += 1
                    self.robot.asserv(-20, -20)
                    
        if self.state == 4:
            if event.name == "asserv":
                if event.type == "done_rot":
                    self.state += 1
                    self.robot.rotate(900)
        
        if self.state == 5:
            if event.name == "bump":
                if event.state == "close":
                    # set odo = ...
                    self.state += 1
                    
                    
        if self.state == 6:
            if event.name == "odo":
                if event.type == "pos":
                    self.state += 1
                    print ("Recalibration terminée !")



