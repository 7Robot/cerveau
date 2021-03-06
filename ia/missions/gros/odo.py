# -*- coding: utf-8 -*-
'''
Created on 30 avr. 2012
'''


from missions.mission import Mission
from events.event import Event


class OdoMission(Mission):
    def __init__(self, robot, can, ui):
        super(self.__class__,self).__init__(robot, can, ui)
         
        self.state = None # pas de recalibration en cour
        self.brd = False # par defaut, pas de broadcast de l'odo
        self.req = False # une requête d'odo est en cour
        self.dest = [] # dest des request

        self.pos = self.robot.pos
        self.rot = self.robot.rot
        self.target_pos = self.robot.pos
        self.target_rot = self.robot.rot

    def broadcast(self, state = True):
        if state != self.brd:
            self.brd = state
            if state:
                self.can.send("odo unmute")
            else:
                self.can.send("odo mute")

    def set(self, callback, **value):
        self.state = "calibrating"
        self.callback = callback
        self.value = value
        self.request()

    def request(self, callback = None):
        if callback != None:
            self.dest.append(callback)
        if not self.req and not self.brd:
            self.req = True
            self.can.send("odo request")
            self.create_timer(500)

    def process_event(self, event):
        if event.name == "timer":
            if self.req:
                self.can.send("odo request")
                self.create_timer(500)
        
        # events geres quelque soit l'etat
        elif event.name == "odo" and event.type == "pos":
            if self.state == "calibrating":
                if not self.brd:
                    self.state = None
                    self.send_event(Event("odo", "done", self.callback))
                else:
                    self.state = "calibrated"
                #print("Calibrating")
                #print("Old pos: %s %d" %(self.move.pos,
                #    self.move.rot))
                #print("Old target: %s %d" %(self.move.target_pos,
                #    self.target_rot))
                for axe in self.value:
                    if axe == "x":
                        event.pos.x = self.value["x"]
                        #self.logger.info("[target] pos.x: %d" %self.value["x"])
                        # TODO remove le logger
                        self.target_pos.x = self.value["x"]
                    elif axe == "y": 
                        event.pos.y = self.value["y"]
                        #self.logger.info("[target] pos.y: %d" %self.value["y"])
                        # TODO remove le logger
                        self.target_pos.y = self.value["y"]
                    elif axe == "rot":
                        event.rot = self.value["rot"]
                        self.target_rot = self.value["rot"]

                #print(self.move)
                self.pos = event.pos
                self.rot = event.rot
                #print("New pos: %s %d" %(self.move.pos,
                #    self.move.rot))
                #print("New target: %s %d" %(self.move.target_pos,
                #    self.move.target_rot))
                self.can.send("odo set %d %d %d"
                        % (event.pos.x/10, event.pos.y/10,
                            (event.rot+72000)%36000))


                #self.send_event(Event("odo", "done", self.callback))
            elif self.state == "calibrated":
                self.state = None
                self.send_event(Event("odo", "done", self.callback))
            else:
                self.pos = event.pos
                self.rot = event.rot
            self.req = False

            if len(self.dest) > 0:
                event.dest = self.dest
                event.type = "answer"
                self.send_event(event)
                #self.send_event(Event("odo", "pos", self.dest, **{"pos":
                #    event.pos, "rot": event.rot}))
