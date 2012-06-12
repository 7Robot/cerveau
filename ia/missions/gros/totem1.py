# -*- coding: utf-8 -*-
u'''
Created on 13 mai 2012
'''

from events.event import Event
from robots.robot import Robot
from missions.mission import Mission
class Totem1Mission(Mission):
    def __init__(self, robot, can, ui):
        super(self.__class__,self).__init__(robot, can, ui)
        
    def process_event(self, event):
        if self.state == 0:
            if event.name == u"start":
                self.state += 1
                self.move.forward(self, 5500) # on sort du depart

        elif self.state == 1:
            if event.name == u"move" and event.type == u"done":
                self.state += 1
                self.move.rotate(self, 27000, True) # on tourne vers les bouteilles

        elif self.state == 2:
            if event.name == u"move" and event.type == u"done":
                self.state += 1
                #self.move.forward(self, 4700) # on avance vers le totem
                if Robot.side == u'violet':
                    self.move.reach_y(self, 3150) # NIM: c’était 2950 33/240
                else:
                    self.move.reach_y(self, 2900) # NIM: c’était 2950

        elif self.state == 3:
            if event.name == u"move" and event.type == u"done":
                self.state += 1
                self.move.rotate(self, -Robot.vrille(), True) # on tourne vers le totem

        elif self.state == 4:
            if event.name == u"move" and event.type == u"done":
                self.state += 1
                self.can.send(u"ax 2 angle set 508")
                self.missions[u"threshold"].activate(2, False)
                if not self.odo.brd:
                    self.can.send(u"odo unmute")
                self.move.speed(35)

        elif self.state == 5:
            if event.name == u"odo" and event.type == u"pos":
                if event.pos.x > -1500:
                    self.state += 1
                    self.missions[u"threshold"].activate(2, True)
                    self.move.stop(self)

        elif self.state == 6:
            if event.name == u"move" and event.type == u"done":
                self.state += 1
                self.can.send(u"ax 2 angle set 0")
                self.create_timer(200)
                
        elif self.state == 7:
            if event.name == u"timer":
                self.state += 1
                self.missions[u"speedrotate"].start(0, 50)

        elif self.state == 8:
            if event.name == u"odo" and event.type == u"pos":
                if event.rot > 17000 and event.rot < 32000:
                    self.state += 1
                    self.missions[u"speedrotate"].stop(self)

        elif self.state == 9:
            if event.name == u"speedrotate" and event.type == u"done":
                if not self.odo.brd:
                    self.state += 1
                    self.can.send(u"odo mute")
                    self.logger.info(u"Bad orientation (%d), adjusting ..."
                            %self.odo.rot)
                    self.move.rotate(self, 20100, True)

        elif self.state == 10:
            if event.name == u"move" and event.type == u"done":
                self.state += 1
                self.move.reach_x(self, -12000)

        elif self.state == 11:
            if event.name == u"move" and event.type == u"done":
                self.state += 0.5
                self.can.send(u"ax 2 angle set 1023")
                self.create_timer(2500)

        elif self.state == 11.5:
            if event.name == u"timer":
                self.state += 0.5
                self.move.forward(self, -4000)

        elif self.state == 12:
            if event.name == u"move" and event.type == u"done":
                self.state += 1
                self.can.send(u"ax 2 angle set 0")
                self.move.rotate(self, 27000, True)

        elif self.state == 13:
            if event.name == u"move" and event.type == u"done":
                self.state = 13.05
                self.move.reach_y(self, 8000)

        elif self.state == 13.05:
            if event.name == u"move" and event.type == u"done":
                self.state = 13.1
                self.move.speed(-15)

        elif self.state == 13.1:
            self.logger.info(u"event", event)
            if event.name == u"bump" and event.state == u"close":
                self.state += 0.1
                self.create_timer(self.robot.pos_timer)

        elif self.state == 13.2:
            if event.name == u"timer":
                self.state += 0.1
                self.move.stop(self)

        elif self.state == 13.3:
            if e.name == u"move" and e.type == u"done":
                self.state = 0.1
                self.can.send(u"asserv off")
                self.odo.set(self, **{u"y": 10000 - self.robot.dimensions[u"back"], u"rot": 27000 + Robot.vrille()})

        elif self.state == 13.4:
            if e.name == u"odo" and e.type == u"done":
                self.state = 14
                self.can.send(u"asserv on")
                self.move.forward(self, 1300)

        elif self.state == 14:
            if event.name == u"move" and event.type == u"done":
                self.state += 1
                self.move.rotate(self, 0, True)

        elif self.state == 15:
            if event.name == u"move" and event.type == u"done":
                self.state += 0.5
                self.move.reach_x(self, -13000)

        elif self.state == 15.5:
            if event.name == u"move" and event.type == u"done":
                self.state += 0.5
                self.move.speed(-15)

        elif self.state == 16:
            if event.name == u"bump" and event.state == u"close":
                self.state += 1
                self.create_timer(self.robot.pos_timer)

        elif self.state == 17:
            if event.name == u"timer":
                self.state += 1
                self.move.stop(self)

        elif self.state == 18:
            if event.name == u"move" and event.type == u"done":
                self.state += 1
                self.can.send(u"asserv off")
                self.odo.set(self, **{u"x": self.robot.dimensions[u"back"] - 15000, u"rot": Robot.vrille() })

        elif self.state == 19:
            if event.name == u"odo" and event.type == u"done":
                self.can.send(u"asserv on")
                self.send_event(Event(u"totem", u"done"))
