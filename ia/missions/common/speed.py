# -*- coding: utf-8 -*-
u'''
Created on 5 mai 2012
'''


from __future__ import division
from events.event import Event

from missions.mission import Mission
from robots.robot import Robot
class SpeedMission(Mission):
    def __init__(self, robot, can, ui):
        super(self.__class__,self).__init__(robot, can, ui)
        u'''
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
        self.state = u"repos"


    # s'orienter dans la direction rot_target
    def start(self, speed, curt = False, callback_autoabort = None):
        if self.state == u"repos":
            self.curt = curt
            self.speed = speed
            self.callback = callback_autoabort
            self.autoabort = callback_autoabort != None
            self.can.send(u"asserv ticks reset")
            if ((self.captor.front and speed > 0)
                    or (self.captor.back and speed < 0)):
                self.state = u"paused"
                if self.speed != 0:
                    self.missions[u"threshold"].sensivity(0.6)
            else:
                self.state = u"run"
                if self.speed != 0:
                    sens = abs(self.speed) / 50
                    self.missions[u"threshold"].sensivity(sens)
                if self.curt:
                    self.can.send(u"asserv speed %d %d curt" %(self.speed, self.speed))
                else:
                    self.can.send(u"asserv speed %d %d" %(self.speed, self.speed))
             
    def change(self, speed):
        self.speed = speed
        if self.state == u"run":
            self.can.send(u"asserv speed %d %d curt" %(speed, speed))
            if self.speed != 0:
                sens = abs(self.speed) / 50
                self.missions[u"threshold"].sensivity(sens)

    def stop(self, callback):
        self.callback = callback
        if self.state == u"run":
            self.state = u"stopping"
            self.can.send(u"asserv stop")
        elif self.state == u"aborting" or self.state == u"pausing":
            self.state = u"stopping"
        elif self.state == u"paused":
            self.can.send(u"asserv ticks request")
            self.state = u"stopped"

    def pause(self):
        if self.state == u"run":
            if self.autoabort:
                self.state = u"aborting"
            else:
                self.state = u"pausing"
            self.can.send(u"asserv stop")

    def resume(self):
        # FIXME il est peut-être possible de redémarrer sans attendre le asserv done
        if self.state == u"paused":
            if ((not self.captor.front and self.speed > 0) \
                    or (not self.captor.back and self.speed < 0)):
                self.state = u"run"
                if self.speed != 0:
                    sens = abs(self.speed) / 50
                    self.missions[u"threshold"].sensivity(sens)
                if self.curt:
                    self.can.send(u"asserv speed %d %d curt" %(self.speed, self.speed))
                else:
                    self.can.send(u"asserv speed %d %d" %(self.speed, self.speed))

    def process_event(self, event):
        if event.name == u"captor":
            if self.state != u"repos":
                if ((event.pos == u"front" and self.speed > 0) \
                        or (event.pos == u"back" and self.speed < 0)):
                    if event.state == u"start":
                        self.resume()
                    else:
                        self.pause()

        elif event.name == u"asserv" and event.type == u"done":
            if self.state == u"pausing":
                self.state = u"paused"
                if self.speed != 0:
                    self.missions[u"threshold"].sensivity(0.6)
                self.resume()
            elif self.state == u"stopping":
                self.state = u"stopped"
                self.can.send(u"asserv ticks request")
            elif self.state == u"aborting":
                self.state = u"aborted"
                self.can.send(u"asserv ticks request")

        if event.name == u"asserv" and event.type == u"ticks" and event.cmd == u"answer":
            if self.state == u"stopped":
                self.state = u"repos"
                self.state = u"repos"
                self.missions[u"threshold"].sensivity(1)
                self.send_event(Event(u"speed", u"done", self.callback, **{u"value": event.value}))
            elif self.state == u"aborted":
                self.state = u"repos"
                self.missions[u"threshold"].sensivity(1)
                self.send_event(Event(u"speed", u"aborted", self.callback, **{u"value": event.value}))
