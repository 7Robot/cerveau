# -*-coding:UTF-8 -*

from missions.mission import Mission

class PositioningMission(Mission):

    def process_event(self, e):
        if self.state == 0:
            if e.name == "start":
                self.robot.rotate(-900);
                self.state += 1

        elif self.state == 1:
            if e.name == "asserv" and e.type == "done":
                self.robot.asserv(20, 20)
                self.state += 1
                                    
        elif self.state == 2:
            if e.name == "bump" and e.state == "close":
                self.create_timer(700)
                self.state += 1
                    
        elif self.state == 3:
            if e.name == "timer":
                self.robot.forward(-1500)
                self.state += 1
                    
        elif self.state == 4:
            if e.name == "asserv" and e.type == "done":
                self.robot.rotate(900)
                self.state += 1
                    
        elif self.state == 5:
            if e.name == "asserv" and e.type == "done":
                self.robot.asserv(-20, -20)
                self.state += 1

        elif self.state == 6:
            if e.name == "bump" and e.state == "close":
                self.create_timer(700)
                self.state += 1
                    
        elif self.state == 7:
            if e.name == "timer":
                self.robot.forward(1000)
                # TODO envoit message à petit
                self.state += 1
                print("Gro en position !")
        
 #       if self.state == 3:
 #           if event.name == "asserv":
 #               if event.type == "done_dist":
 #                   self.state += 1
 #                   self.robot.asserv(-20, -20)
 #                   
 #       if self.state == 4:
 #           if event.name == "asserv":
 #               if event.type == "done_rot":
 #                   self.state += 1
 #                   self.robot.rotate(900)
 #       
 #       if self.state == 5:
 #           if event.name == "bump":
 #               if event.state == "close":
 #                   # set odo = ...
 #                   self.state += 1
 #                   
 #                   
 #       if self.state == 6:
 #           if event.name == "odo":
 #               if event.type == "pos":
 #                   self.state += 1
 #                   print ("Recalibration terminée !")
 #


