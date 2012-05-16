# -*- coding: utf-8 -*-
'''
Created on 5 mai 2012
'''


from events.event import Event

from missions.mission import Mission
class SpeedMission(Mission):
    def __init__(self, robot, can, ui):
        super(self.__class__,self).__init__(robot, can, ui)
        self.state = "repos"
        self.free_way = True


    # s'orienter dans la direction rot_target
    def start(self, speed, curt = False, callback_autoabort = None):
        if self.state == "repos":
            self.curt = curt
            self.speed = speeda
            callback = callback_autoabort
            self.autoabort = callback_autoabort != None
            self.can.send("asserv ticks reset")
            self.state = "run"
            if self.curt:
                self.can.send("asserv speed %d %d curt" %(self.speed, self.speed))
            else:
                self.can.send("asserv speed %d %d" %(self.speed, self.speed))
             
    def change(self, speed):
        self.speed = speed
        if self.state == "run":
            self.can.send("asserv speed %d %d curt" %(speed, speed))

    def stop(self, callback):
        if self.state == "run":
            self.callback = callback
            self.state = "stopping"
            self.can.send("asserv stop")

    def pause(self):
        if self.state == "run":
            self.state = "pausing"
            self.can.send("asserv stop")

    def resume(self):
        if self.state == "waiting" and self.freeway:
            self.state == "run"
            if self.curt:
                self.can.send("asserv speed %d %d curt" %(self.speed, self.speed))
            else:
                self.can.send("asserv speed %d %d" %(self.speed, self.speed))
             

    def process_event(self, event):
        if event.name == "captor" \
                and ((event.pos == "front" and self.dist > 0) \
                  or (event.pos == "back"  and self.dist < 0)):
            if event.state == "start":
                self.free_way = True
                if not self.autoabort:
                    self.resume()
                else:
                    self.state = "repos"
                    self.send_event(Event("speed", "aborted", self.callback))
            else:
                self.free_way = False
                self.pause()


        elif event.name == "asserv" and event.type == "done":
            if self.state == "run" or self.state == " # FIXME a finir

            if event.name == "asserv" and event.type == "done":
                self.state = "stopped"
                self.can.send("asserv ticks request")

        elif self.state == "pausing

        elif self.state == "stopped":
            if event.name == "asserv" and event.type == "ticks" and event.cmd == "answer":
                self.state = "repos"
                self.send_event(Event("speed", "done", self.callback, **{"value": event.value}))
                
