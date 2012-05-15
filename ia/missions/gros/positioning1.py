# -*-coding:UTF-8 -*

from missions.mission import Mission

from events.event import Event
from robots.robot import Robot

class Positioning1Mission(Mission):
    def __init__(self, robot, can, ui):
        super(self.__class__,self).__init__(robot, can, ui)

    def start(self):
        if self.state == 0:
            self.state += 1
            self.logger.info("Positionnement de Gros")
            self.send_event(Event("start", None, self))

    def process_event(self, e):
        if self.state == 1 and e.name == "start":
            self.state += 1
            self.move.speed(-self.robot.pos_speed)
            
        elif self.state == 2:
            if e.name == "bump" and e.state == "close":
                self.state += 1
                self.create_timer(self.robot.pos_timer)
                    
        elif self.state == 3:
            if e.name == "timer":
                self.state += 0.5
                self.move.stop(self)

        elif self.state == 3.5:
            if e.name == "move" and e.type == "done":
                self.state += 0.5
                self.can.send("asserv off")
                self.odo.set(self, **{"y": 10000 - self.robot.dimensions["back"], "rot": 27000 + self.robot.vrille})

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
                self.move.speed(-self.robot.pos_speed)

        elif self.state == 7:
            if e.name == "bump" and e.state == "close":
                self.state += 0.5
                self.create_timer(self.robot.pos_timer)

        elif self.state == 7.5:
            if e.name == "timer":
                self.state += 0.5
                self.move.stop(self)
                    
        elif self.state == 8:
            if e.name == "move" and e.type == "done":
                self.state += 1
                self.can.send("asserv off")
                self.odo.set(self, **{"x": self.robot.dimensions["back"] - 15000, "rot": self.robot.vrille})

        elif self.state == 9:
            if e.name == "odo" and e.type == "done":
                self.state += 1
                self.can.send("asserv on")
                self.move.forward(self, 300)

        elif self.state == 10:
            if e.name == "move" and e.type == "done":
                self.state = 0
                self.logger.info("Gros en position !")
                self.send_event(Event("positioning", "done"))
