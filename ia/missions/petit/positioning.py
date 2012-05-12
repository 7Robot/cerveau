# -*-coding:UTF-8 -*

from missions.mission import Mission

class PositioningMission(Mission):
    def __init__(self, robot, can, ui):
        super(self.__class__,self).__init__(robot, can, ui)

    def start(self):
        if self.state == 0:
            self.move.rotate(self, -9000)
            self.state += 1

    def process_event(self, e):
        if self.state == 1:
            if e.name == "move" and e.type == "done":
                self.state += 1
                self.move.speed(-20, -20)
                                    
        elif self.state == 2:
            if e.name == "bump" and e.state == "close":
                self.state += 1
                self.create_timer(700)
                    
        elif self.state == 3:
            if e.name == "timer":
                self.state += 0.5
                self.move.stop(self)

        elif self.state == 3.5:
            if e.name == "move" and e.type == "done":
                self.state += 0.5
                self.odo.set(self, **{"y": self.robot.dimensions["back"] - 10000, "rot": 27000})

        elif self.state == 4:
            if e.name == "odo" and e.type == "done":
                self.state += 1
                self.move.forward(self, 1500)
                    
        elif self.state == 5:
            if e.name == "move" and e.type == "done":
                self.state += 1
                self.move.rotate(self, 9000)
                    
        elif self.state == 6:
            if e.name == "move" and e.type == "done":
                self.state += 1
                self.move.speed(-20, -20)

        elif self.state == 7:
            if e.name == "bump" and e.state == "close":
                self.state += 0.5
                self.odo.set(self, **{"x": self.robot.dimensions["back"] - 15000, "rot": 0})

        elif self.state == 7.5:
            if e.name == "odo" and e.type == "done":
                self.state += 0.5
                self.create_timer(700)
                    
        elif self.state == 8:
            if e.name == "timer":
                self.state += 1
                self.move.stop(self)

        elif self.state == 9:
            if e.name == "move" and e.type == "done":
                self.state += 1
                self.move.forward(self, 5000)

        elif self.state == 10:
            if e.name == "move" and e.type == "done":
                self.state += 1
                self.create_timer(20000) # FIXME à mesurer
                self.logger.info("Petit en attente de positionnement de gros")

        elif self.state == 11:
            if e.name == "robot":
                self.state += 1
                self.move.forward(self, -2500)
            elif e.name == "timer":
                self.state += 1
                self.logger.warning("Pas de réponse de gros !")
                self.move.forward(self, -2500)

        elif self.state == 12:
            if e.name == "move" and e.type == "done":
                self.state = 0
                self.logger.info("Petit en position !")
