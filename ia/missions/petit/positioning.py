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
            self.missions[u"threshold"].activate(1, False)
            self.missions[u"threshold"].activate(2, False)
            self.missions[u"threshold"].activate(8, False)
            self.state += 1

    def process_event(self, e):
        if self.state == 0:
            if e.name == u"timer":
                self.state = 2
                self.missions[u"speed"].start( -20)
        elif self.state == 2:
            if e.name == u"bump" and e.state == u"close":
                self.state += 1
                self.create_timer(700)
            elif e.name == u"bump" and e.pos == u"alim" \
                    and e.state == u"close":
                self.missions[u"speed"].start(-20)
                    
        elif self.state == 3:
            if e.name == u"timer":
                self.state += 1
                self.missions[u"speed"].stop(self)

        elif self.state == 4:
            if e.name == u"speed" and e.type == u"done":
                self.state += 1
                self.missions[u"forward"].start(self, 1800)
                    
        elif self.state == 5:
            if e.name == u"forward" and e.type == u"done":
                self.state += 1
                self.missions[u"rotate"].start(self, 9000)
                    
        elif self.state == 6:
            if e.name == u"rotate" and e.type == u"done":
                self.state += 1
                self.missions[u"speed"].start(-20)

        elif self.state == 7:
            if e.name == u"bump" and e.state == u"close":
                self.state += 0.5
                self.create_timer(700)

        elif self.state == 7.5:
            if e.name == u"timer":
                self.state += 0.5
                self.missions[u"speed"].stop(self)
                    
        elif self.state == 8:
            if e.name == u"speed" and e.type == u"done":
                self.state += 2
                self.missions[u"forward"].start(self, 6000)

        elif self.state == 10:
            if e.name == u"forward" and e.type == u"done":
                self.state += 1
                self.logger.info(u"Petit en attente de positionnement de Gros")

        elif self.state == 11:
            if (e.name == u"robot" and e.type == u"ready") \
                    or (e.name == u"bump" and e.state == u"close"):
                self.state += 1
                self.missions[u"forward"].start(self, -3100)

        elif self.state == 12:
            if e.name == u"forward" and e.type == u"done":
                self.state = 0
                self.missions[u"threshold"].activate(1, True)
                self.missions[u"threshold"].activate(2, True)
                self.missions[u"threshold"].activate(8, True)
                self.logger.info(u"Petit en position !")
                self.send_event(Event(u"positioning", u"done"))
