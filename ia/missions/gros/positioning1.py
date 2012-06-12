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
            self.logger.info(u"Positionnement de Gros")
            self.send_event(Event(u"start", None, self))

    def process_event(self, e):
        if self.state == 1 and e.name == u"start":
            self.state += 1
            self.missions[u"threshold"].activate(1, False)
            self.missions[u"threshold"].activate(2, False)
            self.missions[u"threshold"].activate(8, False)
            self.move.speed(-self.robot.pos_speed)
            
        elif self.state == 2:
            if e.name == u"bump" and e.state == u"close" and e.pos == u"back":
                self.state += 1
                self.create_timer(self.robot.pos_timer)
            elif e.name == u"bump" and e.state == u"open" and e.pos == u"alim":
                self.move.speed(-self.robot.pos_speed)
                    
        elif self.state == 3:
            if e.name == u"timer":
                self.state += 0.5
                self.move.stop(self)

        elif self.state == 3.5:
            if e.name == u"move" and e.type == u"done":
                self.state += 0.5
                self.can.send(u"asserv off")
                self.odo.set(self, **{u"y": 10000 - self.robot.dimensions[u"back"], u"rot": 27000 + Robot.vrille()})

        elif self.state == 4:
            if e.name == u"odo" and e.type == u"done":
                self.state += 1
                self.can.send(u"asserv on")
                self.move.forward(self, 1300)
                    
        elif self.state == 5:
            if e.name == u"move" and e.type == u"done":
                self.state += 1
                self.move.rotate(self, 9000)
                    
        elif self.state == 6:
            if e.name == u"move" and e.type == u"done":
                self.state += 1
                self.move.speed(-self.robot.pos_speed)

        elif self.state == 7:
            if e.name == u"bump" and e.state == u"close":
                self.state += 0.5
                self.create_timer(self.robot.pos_timer)

        elif self.state == 7.5:
            if e.name == u"timer":
                self.state += 0.5
                self.move.stop(self)
                    
        elif self.state == 8:
            if e.name == u"move" and e.type == u"done":
                self.state += 1
                self.can.send(u"asserv off")
                self.odo.set(self, **{u"x": self.robot.dimensions[u"back"] - 15000, u"rot": Robot.vrille()})

        elif self.state == 9:
            if e.name == u"odo" and e.type == u"done":
                self.state += 1
                self.can.send(u"asserv on")
                self.move.forward(self, 300)

        elif self.state == 10:
            if e.name == u"move" and e.type == u"done":
                self.state = 0
                self.logger.info(u"Gros en position !")
                self.missions[u"threshold"].activate(1, True)
                self.missions[u"threshold"].activate(2, True)
                self.missions[u"threshold"].activate(8, True)
                self.send_event(Event(u"positioning", u"done"))
