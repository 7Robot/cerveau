# -*- coding: utf-8 -*-
'''
Created on 5 mai 2012
'''

from events.internal import ForwardDoneEvent
from math import cos, sin, pi

from missions.mission import Mission
class ForwardMission(Mission):
    def __init__(self, robot):
        super(self.__class__,self).__init__(robot)
        self.state = "repos"
        self.free_way = { 0: True, 1: True, 2: True, 3: True }

    def disable(self):
        self.state = "repos"

    def way_is_free(self):
        free_way = True
        sensors = [] 
        if self.dist > 0:
            sensors = [0, 1, 2]
        else:
            sensors = [3]
        for key in sensors:
            if not self.free_way[key]:
                free_way = False
                break
        return free_way
        
    def move_forward(self):
        if self.state == "repos":
            # première étape : récupérer la position actuelle
            self.robot.can_send("odo request")
            self.state = "updating"

    def resume(self):
        if self.decrement:
            if self.way_is_free():
                self.state = "forwarding"
                self.robot.send_can("asserv dist %d" %self.dist)

    def stop(self):
        self.robot.send_can("asserv stop")
        self.decrement = False
        self.state = "waiting"
        
        
    def process_event(self, event):
        if          self.state == "updating"
                and event.name == "odo"
                and event.type == "answer":
            # màj de la position
            self.robot.pos = event.pos
            self.robot.rot = event.rot
            # détermination du mouvement à effecuter
            self.dist  = (self.robot.pos_target - self.robot.pos).norm
            self.state = "forwarding" # sioux : 0 -> 1 ou 2 -> 3
            self.robot.send_can("asserv dist %d" %self.dist)
        elif event.name == "rangefinder" and event.id in [1,2]:
            self.free_way[event.id] = (event.pos == "over")
            if self.state == "forwarding" and event.pos == "under":
                self.stop()
            if self.state == "waiting" and event.pos == "over":
                self.resume()
        elif event.name == "turret" and e.type == "answer":
            hysteresis = 0
            if not self.free_way[0]: # 
                hysteresis = 1
            self.free_way[0] = True
            for i in range(len(e.angle)):
                e.dist[i] -= 8
                obs_x = e.dist[i]*cos(e.angle[i]/180*pi)
                obs_y = e.dist[i]*sin(e.angle[i]/180*pi)
                # la tourelle laser est à 8cm du bord droit
                # 15cm du bord gauche  TODO: mettre ces params dans le robot
                #print("X: %d, Y: %d, histeresis: %d"
                #        %(obs_x, obs_y, self.histeresis))
                if  obs_x < 10+8*self.histeresis and obs_x > -12-8*self.histeresis \
                and obs_y < 30+4*self.histeresis:
                    self.free_way[0] = False
                    break

        if self.state == "forwarding":
            if event.name == "asserv":
                if event.type == "done":
                    # on a pu aller là où on voulait aller
                    self.state = "repos"
                    self.dispatch.add_event(ForwardDoneEvent())
                    
        elif self.state == "waiting":
            if          event.name == "asserv" \
                    and event.type == "int_dist" \
                    and self.decrement == False:
                self.dist -= event.value
                self.decrement = True
                self.resume()

