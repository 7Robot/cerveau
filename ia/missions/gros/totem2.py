# -*- coding: utf-8 -*-
'''
Created on 13 mai 2012
'''

from events.event import Event

from missions.mission import Mission
class Totem2Mission(Mission):
    def __init__(self, robot, can, ui):
        super(self.__class__,self).__init__(robot, can, ui)
        
    def process_event(self, event):
        if self.state == 0:
            if event.name == "start":
                self.state += 1
                self.move.forward(self, 5000) # on sort du depart

        elif self.state == 1:
            if event.name == "move" and event.type == "done":
                self.state += 1
                self.move.rotate(self, 27000, True) # on tourne vers les bouteilles

        elif self.state == 2:
            if event.name == "move" and event.type == "done":
                self.state += 1
                self.move.reach_y(self, -3000)

        elif self.state == 3:
            if event.name == "move" and event.type == "done":
                self.state += 1
                self.move.rotate(self, 0, True) # on tourne vers le totem

        elif self.state == 4:
            if event.name == "move" and event.type == "done":
                self.state += 1
                self.can.send("ax 1 angle set 508")
                self.can.send("rangefinder 2 threshold 0")
                if not self.odo.brd:
                    self.can.send("odo unmute")
                self.move.speed(35)

        elif self.state == 5:
            if event.name == "odo" and event.type == "answer":
                if event.pos.x > -1500:
                    self.state += 1
                    self.can.send("rangefinder 2 threshold %d"
                            % self.robot.rangefinder[2])
                    self.move.stop(self)

        elif self.state == 6:
            if event.name == "move" and event.type == "done":
        #        self.state += 1
                self.state += 2
                self.can.send("ax 1 angle set 0")
        #        self.create_timer(1000)
                
        #elif self.state == 7:
        #    if event.name == "timer":
        #        self.state += 1
                self.missions["speedrotate"].start(80, 0)

        elif self.state == 8:
            if event.name == "odo" and event.type == "pos":
                if event.rot < 16000 and event.rot > 9000:
                    self.state += 1
                    self.missions["speedrotate"].stop(self)

        elif self.state == 9:
            if event.name == "speedrotate" and event.type == "done":
                if self.odo.rot < 13000 and self.odo.rot > 11000:
                    self.state += 3
                    self.move.reach_x(self, -12500)
                else:
                    self.state += 1
                    self.logger.info("Bad orientation (%d), adjusting ..."
                            %self.odo.rot)
                    self.move.rotate(self, 12000, True)

        elif self.state == 10:
            if event.name == "move" and event.type == "done":
                self.state += 1
                self.move.reach_x(self, -12500)

        elif self.state == 11:
            if event.name == "move" and event.type == "done":
                self.state += 1
                self.move.forward(self, -2000)
                self.send_event(Event("totem", "done"))

        #elif self.state == 12:
        #    if event.name == "move" and event.type == "done":
        #        self.state += 1
        #        self.missions["speedrotate"].start(-50, -25)

        #elif self.state == 13:
        #    if event.name == "odo" and event.type == "pos":
        #        if event.rot < 20000:
        #            self.state += 1
        #            self.missions["speedrotate"].stop(self)

        #elif self.state == 14:
        #    if event.name == "speedrotate" and event.type == "done":
        #        if not self.odo.brd:
        #            self.can.send("odo mute")
        #        if self.odo.rot < 17000 and self.odo.rot > 19000:
        #            self.send_event(Event("totem", "done"))
        #            self.state = 0
        #        else:
        #            self.state += 1
        #            self.logger.info("Bad orientation (%d), adjusting ..."
        #                    %self.odo.rot)
        #            self.move.rotate(self, 18000, True)

        #elif self.state == 15:
        #    if event.name == "move" and event.type:
        #        self.send_event(Event("totem", "done"))
