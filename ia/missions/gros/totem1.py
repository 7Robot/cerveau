# -*- coding: utf-8 -*-
'''
Created on 13 mai 2012
'''

from missions.mission import Mission
class Totem1Mission(Mission):
    def __init__(self, robot, can, ui):
        super(self.__class__,self).__init__(robot, can, ui)
        
    def process_event(self, event):
        if self.state == 0:
            if event.name == "start":
                self.state += 1
                self.move.forward(self, 5700) # on sort du départ

        elif self.state == 1:
            if event.name == "move" and event.type == "done":
                self.state += 1
                self.move.rotate(self, -9000) # on tourne vers les bouteilles

        elif self.state == 2:
            if event.name == "move" and event.type == "done":
                self.state += 1
                self.move.forward(self, 4300) # on avance vers le totem

        elif self.state == 3:
            if event.name == "move" and event.type == "done":
                self.state += 1
                self.move.rotate(self, 9000) # on tourne vers le totem

        elif self.state == 4:
            if event.name == "move" and event.type == "done":
                self.state += 1
                self.can.send("ax 2 angle set 508")
                self.can.send("rangefinder 2 threshold 0")
                self.move.speed(20, 20)

        elif self.state == 5:
            if event.name == "odo" and event.type == "pos":
                if event.pos.x > -1500:
                    self.state += 1
                    self.can.send("rangefinder 2 threshold %d"
                            % self.robot.rangefinder[2])
                    self.move.stop(self)

        elif self.state == 6:
            if event.name == "move" and event.type == "done":
                self.state += 1
                self.can.send("ax 2 angle set 0")
                self.create_timer(1000)
                
        elif self.state == 7:
            if event.name == "timer":
                self.state += 1
                self.move.speed(0, 30)

        elif self.state == 8:
            print("Event 8")
            if event.name == "odo" and event.type == "pos":
                print("Angle: %d" %event.rot)
                if event.rot > 27000 and event.rot < 35000:
                    print("STOP ! (%d)" %event.rot)
                    self.state += 1
                    self.move.stop(self)

        elif self.state == 9:
            if event.name == "move" and event.type == "done":
                self.state += 1
                self.missions["forward"].start(self, 14000)

        elif self.state == 10:
            if event.name == "move" and event.type == "done":
                self.state += 1
                self.can.send("ax 2 angle set 1023")
                self.create_timer(1500) 

        elif self.state == 11:
            if event.name == "timer":
                self.state += 1
                self.can.send("ax 2 angle set 0")
