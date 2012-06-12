# -*- coding: utf-8 -*-
u'''
Created on 14 mai 2012
'''

from events.event import Event
from missions import Mission
from robots.robot import Robot

class Double_CheminMission(Mission):
    def __init__(self, robot, can, ui):
        super(self.__class__,self).__init__(robot, can, ui)
        self.went_B = False
        self.tries  = 0
        self.path     = u"A"

    def start(self, callback, dist, avoidance_dist, first_rot = -9000):
        self.missions[u"captor"].dist_y = 9999999
        self.missions[u"captor"].largeur = -6
        self.callback = callback
        self.dist     = dist
        self.avoidance_dist = avoidance_dist
        self.first_rot = first_rot
        self.state    +=1
        self.path     = u"A"
        self.process_event(Event(u"start"))
        self.went_B = False
        self.tries  = 0
        
        
    def process_event(self, e):
        if self.state  == 1:
            if e.name == u"start":
                self.state += 1
                self.tries = 0
                self.missions[u"forward"].start(self, self.dist, True)
                
                
        
        elif self.state == 2:
            if e.name == u"forward" and e.type == u"aborted":
                print u"Received abort !!!!!"
                if self.tries <4 :
                    # Moins de 4 tentatives
                    self.state += 1
                    self.tries += 1
                    self.dist = self.missions[u"forward"].remaining 
                    print u"Remaining", self.missions[u"forward"].remaining
                    if self.path == u"A":
                        self.path = u"B"
                        self.went_B = True
                        self.missions[u"rotate"].start(self, self.first_rot)
                    else:
                        self.path = u"A"
                        self.missions[u"rotate"].start(self,-self.first_rot)                  
                    # Go chemin B
                else:
                    # trop de changements de trajectoire, on abandonne
                    self.state = u"cancel"
                    self.missions[u"forward"].start(self, self.missions[u"forward"].remaining)
                
            elif e.name == u"forward" and e.type == u"done":
                self.state = 100
                self.missions[u"captor"].dist_y  = 0
                self.missions[u"captor"].largeur = 0
                self.send_event(Event(u"double_chemin", u"done", self.callback))
                
        elif self.state == 3:
            if e.name == u"rotate" and e.type == u"done":
                print u"rotated done !!!!!!!!!"
                self.state += 1
                self.missions[u"threshold"].activate(8, False)
                self.missions[u"forward"].start(self, self.avoidance_dist)
                # on se décale de 60 cm
                
        elif self.state == 4:
            print u"state4, waiting", e.name
            if e.name == u"forward" and e.type == u"done":
                self.state += 1
                if self.path == u"A":
                    self.missions[u"rotate"].start(self, self.first_rot)
                else:
                    self.missions[u"rotate"].start(self, -self.first_rot)
                    
        elif self.state == 5:
            if e.name == u"rotate" and e.type == u"done":
                self.state = 2
                self.missions[u"threshold"].activate(8, True)
                self.missions[u"forward"].start(self, self.dist, True)
                
        elif self.state == u"cancel":
            if e.name == u"forward" and e.type == u"done":
                # copy/paste, not nice
                self.state = 100
                self.missions[u"captor"].dist_y  = 0
                self.missions[u"captor"].largeur = 0
                self.send_event(Event(u"double_chemin", u"done", self.callback))
        
                        
        