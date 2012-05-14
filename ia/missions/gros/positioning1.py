# -*-coding:UTF-8 -*

from missions.mission import Mission

from events.internal import MoveEvent
from robots.robot import Robot

class Positioning1Mission(Mission):
    def __init__(self, robot, can, ui):
        super(self.__class__,self).__init__(robot, can, ui)

    def start(self, callback):
        if self.state == 0:
            self.state = 2
            self.callback = callback
            self.logger.info("Positionnement de Gros")
            self.move.speed(-20, -20)

    def process_event(self, e):
        if self.state == 2:
            if e.name == "bump" and e.state == "close":
                self.state += 1
                self.create_timer(300)
                    
        elif self.state == 3:
            if e.name == "timer":
                self.state += 0.5
                self.move.stop(self)

        elif self.state == 3.5:
            if e.name == "move" and e.type == "done":
                self.state += 0.5
                self.can.send("asserv off")
                self.odo.set(self, **{"y": 10000 - self.robot.dimensions["back"], "rot": 27000 + Robot.vrille})

        elif self.state == 4:
            if e.name == "odo" and e.type == "done":
                self.state += 1
                self.can.send("asserv on")
                self.move.forward(self, 1300)
                    
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
                self.create_timer(300)

        elif self.state == 7.5:
            if e.name == "timer":
                self.state += 0.5
                self.move.stop(self)
                    
        elif self.state == 8:
            if e.name == "move" and e.type == "done":
                self.state += 1
                self.can.send("asserv off")
                self.odo.set(self, **{"x": self.robot.dimensions["back"] - 15000, "rot": 0})

        elif self.state == 9:
            if e.name == "odo" and e.type == "done":
                self.state += 1
                self.can.send("asserv on")
                self.move.forward(self, 500)

        elif self.state == 10:
            if e.name == "move" and e.type == "done":
                self.state = 0
                self.logger.info("Gros en position !")
                self.send_event(MoveEvent("done", self.callback))
