# -*- coding: utf-8 -*-
u'''
Created on 13 mai 2012
'''

from events.event import Event

from missions.mission import Mission
class Totem2Mission(Mission):
    def __init__(self, robot, can, ui):
        super(self.__class__,self).__init__(robot, can, ui)
        
    def process_event(self, event):
        if self.state == 0:
            if event.name == u"start":
                self.state += 1
                self.move.reach_x(self, 8000)

        elif self.state == 1:
            if event.name == u"move" and event.type == u"done":
                self.state += 1
                self.move.rotate(self, 27000, True) # on tourne vers le totem

        elif self.state == 2:
            if event.name == u"move" and event.type == u"done":
                self.state += 1
                self.speed(-15)

        elif self.state == 3:
            if event.name == u"bump" and event.status == u"close":
                self.state += 0.1
                self.create_timer(self.robot.pos_timer)

        elif self.state == 3.1:
            if event.name == u"timer":
                self.state += 0.1
                self.move.stop(self)

        elif self.state == 3.2:
            if event.name == u"move" and event.type == u"done":
                self.state += 0.1
                self.can.send(u"asserv off")
                self.odo.set(self, **{u"y": 10000 - self.robot.dimensions[u"back"], u"rot": 27000 + Robot.vrille()})

        elif self.state == 3.3:
            if event.name == u"odo" and event.type == u"done":
                self.state += 0.1
                self.can.send(u"asserv on")
                self.move.reach_y(self, 3000)

        elif self.state == 3.4:
            if event.name == u"move" and event.type == u"done":
                self.state = 4
                self.move.rotate(self, 18000-Robot.vrille(), True)
        elif self.state == 4:
            if event.name == u"move" and event.type == u"done":
                self.state += 1
                self.can.send(u"ax 1 angle set 508")
                self.missions[u"threshold"].activate(1, False)
                if not self.odo.brd:
                    self.can.send(u"odo unmute")
                self.move.speed(35)

        elif self.state == 5:
            if event.name == u"odo" and event.type == u"answer":
                if event.pos.x > -1500:
                    self.state += 1
                    self.missions[u"threshold"].activate(1, True)
                    self.move.stop(self)

        elif self.state == 6:
            if event.name == u"move" and event.type == u"done":
                self.state += 1
                self.can.send(u"ax 1 angle set 0")
                self.move.rotate(self, 4500, True)

        elif self.state == 7:
            if event.name == u"move" and event.type == u"done":
                self.state += 1
                self.move.reach_y(self, 6500)

        elif self.state == 8:
            if event.name == u"move" and event.type == u"done":
                self.state += 1
                self.move.rotate(self, 18000, True)

        elif self.state == 9:
            if event.name == u"move" and event.type == u"done":
                self.state += 1
                self.move.reach_x(self, -8800, True)

        elif self.state == 10:
            if event.name == u"move" and event.type == u"done":
                self.state += 1
                self.ui.send(u"C'est la panic !")
                self.send_event(Event(u"totem", u"done"))
