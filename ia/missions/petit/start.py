# -*- coding: utf-8 -*-
'''
Created on 27 avr. 2012
'''

from missions.mission import Mission
from events.internal import StartEvent

class StartMission(Mission):
    def __init__(self, robot, can, ui):
        super(self.__class__,self).__init__(robot, can, ui)

    def process_event(self, event):
        if self.state == 0:
            self.state +=1
            self.can.send("reset")
            self.create_timer(3000)

        elif self.state == 1:
            if event.name == "timer":
                self.state += 1
                self.odo.broadcast()
                self.can.send("turret unmute")
                self.odo.set(self, **{"x": 0, "y": 0, "rot": 0})

        elif self.state == 2:
            if event.name == "odo" and event.type == "done":
                self.state += 1

        elif self.state == 3:
            if event.name == "bump" and event.state == "close":
                self.state += 1
                self.missions["positioning"].start()

        elif self.state == 4:
            if event.name == "move" and event.type == "done":
                self.state += 1

        elif self.state == 5:
            if event.name == "bump" and event.pos == "leash" \
                    and event.state == "close":
                self.can.send("turret on")
                self.can.send("rangefinder 1 threshold 2800")
                self.can.send("rangefinder 2 threshold 2800")
                self.can.send("rangefinder 8 threshold 2800")
                self.logger.info("Beggining of the match !")


            #self.missions["forward"].start(15000)
            #self.move.forward(self, 5000)
            #self.missions["rotate"].start(9000)
            #self.move.rotate(self, 9000)
            #self.missions["speed"].start(20, 20)
