# -*- coding: utf-8 -*-
'''
Created on 5 mai 2012
'''

from events.internal import ForwardDone

from missions.mission import Mission
class ForwardMission(Mission):
    def __init__(self, robot):
        super(self.__class__,self).__init__(robot)
        self.state = "repos"
        self.free_way = { 0: True, 1: True, 2: True, 3: True }

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
        
    def move_forward(self, dist):
        if self.state == "repos":
            self.dist  = dist
            self.state = "forwarding" # sioux : 0 -> 1 ou 2 -> 3
            self.robot.send_can("asserv dist %d" %self.dist)

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
        if event.name == "rangefinder" and event.id in [1,2]:
            self.free_way[event.id] = (event.pos == "over")
            if self.state == "forwarding" and event.pos == "under":
                self.stop()
            if self.state == "waiting" and event.pos == "over":
                self.resume()
        elif event.name == "turret":
            pass

        if self.state == "forwarding":
            if event.name == "asserv":
                if event.type == "done":
                    # on a pu aller là où on voulait aller
                    self.state = "repos"
                    self.dispatch.add_event(ForwardDone())
                    
        elif self.state == "waiting":
            if          event.name == "asserv" \
                    and event.type == "int_dist" \
                    and self.decrement == False:
                self.dist -= event.value
                self.decrement = True
                self.resume()
