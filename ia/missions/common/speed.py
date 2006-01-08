# -*- coding: utf-8 -*-
'''
Created on 5 mai 2012
'''


from events.event import Event

from missions.mission import Mission
class SpeedMission(Mission):
    def __init__(self, robot, can, ui):
        super(self.__class__,self).__init__(robot, can, ui)
        '''
        repos: rien à faire
        run: la consigne de vitesse à été envyé
        pausing: un arret à été demandé pour cause d'obstacle, on attend
            le asserv done (pour passer en paused)
        paused: on a reçu l'asserv done, on attend soit que l'utilisateur
            demande l'arrêt, soit que la voie soit libre
        stopping: un arret à été demandé par l'utilisateur, on attend
            le asserv done (pour passer en stopped)
        stopped: on a reçu le asserv done, on a envoyé un ticks request
            et on attend le ticks answer (pour envoyé l'event speed done)
        aborting: un arret à été demandé pour cause d'obstacle tous comme
            pausing, mais on est en mode auto abort, on attend le asserv done
            (pour passer en mode aborted)
        aborted: on a reçu le asserv done, on a envoyé un ticks request et on
            attend le ticks answer (pour envoyer un event speed aborted)
        '''
        self.state = "repos"
        self.free_way = {"back": True, "front": True} 


    # s'orienter dans la direction rot_target
    def start(self, speed, curt = False, callback_autoabort = None):
        if self.state == "repos":
            self.curt = curt
            self.speed = speed
            self.callback = callback_autoabort
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
            if self.autoabort:
                self.state = "aborting"
            else:
                self.state = "pausing"
            self.can.send("asserv stop")

    def resume(self):
        # FIXME il est peut-être possible de redémarrer sans attendre le asserv done
        if self.state == "paused":
            if ((self.free_way["front"] and self.speed > 0) \
                    or (self.free_way["back"] and self.speed < 0)):
                self.state == "run"
                if self.curt:
                    self.can.send("asserv speed %d %d curt" %(self.speed, self.speed))
                else:
                    self.can.send("asserv speed %d %d" %(self.speed, self.speed)) 

    def process_event(self, event):
        if event.name == "captor":
            self.free_way[event.pos]  = event.state == "start"
            if self.state != "repos":
                if ((event.pos == "front" and self.speed > 0) \
                        or (event.pos == "back" and self.speed < 0)):
                    if event.state == "start":
                        self.resume()
                    else:
                        self.pause()

        elif event.name == "asserv" and event.type == "done":
            if self.state == "pausing":
                self.state = "paused"
            elif self.state == "stopping":
                self.state = "stopped"
                self.can.send("asserv ticks request")
            elif self.state == "aborting":
                self.state = "aborted"
                self.can.send("asserv ticks request")

        if event.name == "asserv" and event.type == "ticks" and event.cmd == "answer":
            if self.state == "stopped":
                self.state = "repos"
                self.send_event(Event("speed", "done", self.callback, **{"value": event.value}))
            elif self.state == "aborted":
                self.state = "repos"
                self.send_event(Event("speed", "aborted", self.callback, **{"value": event.value}))
