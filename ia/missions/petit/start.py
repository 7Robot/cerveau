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
            self.can.send("rangefinder 1 threshold 2800")
            self.can.send("rangefinder 2 threshold 2800")
            self.can.send("rangefinder 8 threshold 2800")
            self.can.send("turret unmute")
            self.can.send("turret on")
            self.odo.broadcast()
            self.odo.set(self, **{"x": self.robot.pos.x, "y": self.robot.pos.y,
                "rot": self.robot.rot})

        if self.state == 1:
            if event.name == "odo" and event.type == "done":
                self.missions["positioning"].start()





            #self.missions["forward"].start(15000)
            #self.move.forward(self, 5000)
            #self.missions["rotate"].start(9000)
            self.move.rotate(self, 9000)
            #self.missions["speed"].start(40, 20)
