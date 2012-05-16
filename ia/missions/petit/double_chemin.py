# -*- coding: utf-8 -*-
'''
Created on 14 mai 2012
'''

from events.event import Event
from missions import Mission
from robots.robot import Robot

class Double_CheminMission(Mission):
    def __init__(self, robot, can, ui):
        super(self.__class__,self).__init__(robot, can, ui)

    def start(self, callback, dist, avoidance_dist, first_rot = -9000):
        self.missions["captor"].dist_y = 9999999
        self.missions["captor"].largeur = -6
        self.callback = callback
        self.dist     = dist
        self.avoidance_dist = avoidance_dist
        self.first_rot = first_rot
        self.state    +=1
        self.path     = "A"
        self.process_event(Event("start"))
        self.went_B = False
        
        
    def process_event(self, e):
        if self.state  == 1:
            if e.name == "start":
                self.state += 1
                self.missions["forward"].start(self, self.dist, True)
                
                
        
        elif self.state == 2:
            if e.name == "forward" and e.type == "aborted":
                print("Received abort !!!!!")
                self.state += 1
                self.dist = self.missions["forward"].remaining 
                if self.path == "A":
                    self.path = "B"
                    self.went_B = True
                    self.missions["rotate"].start(self, self.first_rot)
                else:
                    self.path = "A"
                    self.missions["rotate"].start(self,-self.first_rot)                  
                # Go chemin B
                
            elif e.name == "forward" and e.type == "done":
                self.state = 100
                self.missions["captor"].dist_y  = 0
                self.missions["captor"].largeur = 0
                self.send_event(Event("double_chemin", "done", self.callback))
                
        elif self.state == 3:
            if e.name == "rotate" and e.type == "done":
                print("rotated done !!!!!!!!!")
                self.state += 1
                for i in [1, 2, 8]:
                    self.can.send("rangefinder %d threshold 0" % i)
                self.missions["forward"].start(self, self.avoidance_dist)
                # on se décale de 60 cm
                
        elif self.state == 4:
            print("state4, waiting", e.name)
            if e.name == "forward" and e.type == "done":
                self.state += 1
                if self.path == "A":
                    self.missions["rotate"].start(self, self.first_rot)
                else:
                    self.missions["rotate"].start(self, -self.first_rot)
                    
        elif self.state == 5:
            if e.name == "rotate" and e.type == "done":
                self.state = 2
                for i in [1, 2, 8]:
                    self.can.send("rangefinder %d threshold %d"
                            % (i, Robot.rangefinder[i]))
                self.missions["forward"].start(self, self.dist, True)
        
                        
        