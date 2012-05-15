# -*-coding:UTF-8 -*

from events.event import Event
from missions.mission import Mission

class PositioningMission(Mission):
    def __init__(self, robot, can, ui):
        super(self.__class__,self).__init__(robot, can, ui)
        self.state = -1

    def start(self):
        if self.state == -1:
            self.create_timer(500)
            self.state += 1

    def process_event(self, e):
        if self.state == 0:
            if e.name == "timer":
                self.state = 2
                self.missions["speed"].start( -20)
        elif self.state == 2:
            if e.name == "bump" and e.state == "close":
                self.state += 1
                self.create_timer(700)
                    
        elif self.state == 3:
            if e.name == "timer":
                self.state += 1
                self.missions["speed"].stop(self)

        elif self.state == 4:
            if e.name == "speed" and e.type == "done":
                self.state += 1
                #self.odo.set(self, **{"y": 10000 - self.robot.dimensions["back"], "rot": 27000})
                self.missions["forward"].start(self, 1800)

#        elif self.state == 4:
#            if e.name == "odo" and e.type == "done":
#                self.state += 1
#                self.move.forward(self, 1800)
                    
        elif self.state == 5:
            if e.name == "forward" and e.type == "done":
                self.state += 1
                self.missions["rotate"].start(self, 9000)
                    
        elif self.state == 6:
            if e.name == "rotate" and e.type == "done":
                self.state += 1
                self.missions["speed"].start(-20)

        elif self.state == 7:
            if e.name == "bump" and e.state == "close":
                self.state += 0.5
                self.create_timer(700)

        elif self.state == 7.5:
            if e.name == "timer":
                self.state += 0.5
                self.missions["speed"].stop(self)
                    
        elif self.state == 8:
            if e.name == "speed" and e.type == "done":
                self.state += 2
                #self.odo.set(self, **{"x": self.robot.dimensions["back"] - 15000, "rot": 0})
                self.missions["forward"].start(self, 6000)

#        elif self.state == 9:
#            if e.name == "odo" and e.type == "done":
#                self.state += 1
#                self.move.forward(self, 8000)

        elif self.state == 10:
            if e.name == "forward" and e.type == "done":
                self.state += 1
                self.logger.info("Petit en attente de positionnement de Gros")

        elif self.state == 11:
            if (e.name == "robot" and e.type == "ready") \
                    or (e.name == "bump" and e.state == "close"):
                self.state += 1
                self.missions["forward"].start(self, -3100)

        elif self.state == 12:
            if e.name == "forward" and e.type == "done":
                self.state = 0
                self.logger.info("Petit en position !")
                self.send_event(Event("positioning", "done"))
