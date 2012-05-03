# -*-coding:UTF-8 -*

from missions.mission import Mission

class PositioningMission(Mission):

    def process_event(self, e):
        if self.state == 0:
            if e.name == "start":
                self.robot.rotate(9000);
                self.state += 1

        elif self.state == 1:
            if e.name == "asserv" and e.type == "done":
                self.robot.asserv(-20, -20)
                self.state += 1
                                    
        elif self.state == 2:
            print(2)
            if e.name == "bump" and e.state == "close":
                print(2.5)
                self.create_timer(700)
                self.state += 1
                    
        elif self.state == 3:
            if e.name == "timer":
                self.robot.forward(1500)
                self.state += 1
                    
        elif self.state == 4:
            if e.name == "asserv" and e.type == "done":
                self.robot.rotate(-9000)
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
                self.create_timer(20000) # FIXME à mesurer
                self.robot.forward(5000)
                self.state += 1
                print("Petit en attente de positionnement de gros")

        elif self.state == 8:
            if e.name == "robot":
                self.robot.forward(-2500)
                self.state += 1
            elif e.name == "timer":
                print("Pas de réponse de gros !")
                self.robot.forward(-2500)
                self.state += 1

        elif self.state == 9:
            if e.name == "asserv" and e.state == "done":
                print("Petit en position !")
                self.state += 1
