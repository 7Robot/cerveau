# -*- coding: utf-8 -*-
u'''
Created on 5 mai 2012
'''


from __future__ import division
from events.event import Event
from robots.robot import Robot

from missions.mission import Mission
class SpeedRotateMission(Mission):
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
    def start(self, left, right, callback_autoabort = None):
        if self.state == u"repos":
            self.left = left
            self.right = right
            self.callback = callback_autoabort
            self.autoabort = callback_autoabort != None
            if ((self.captor.front and (self.left+self.right) > 0)
                    or (self.captor.back and (self.left+self.right) < 0)):
                self.state = u"paused"
                self.missions[u"threshold"].sensivity(0.6)
            else:
                self.state = u"run"
                self.missions[u"threshold"].sensivity(abs(self.left+self.right) / 100.0)
                self.can.send(u"asserv speed %d %d" %(self.left, self.right))
             
    def change(self, speed):
        if self.state != u"repos":
            self.speed = speed 
            self.missions[u"threshold"].sensivity(abs(self.left+self.right) / 100)
            if self.state == u"run":
                self.can.send(u"asserv speed %d %d" %(self.left, self.right))

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
            self.missions[u"threshold"].sensivity(0.6)

    def resume(self):
        # FIXME il est peut-être possible de redémarrer sans attendre le asserv done
        if self.state == u"paused":
            if ((not self.captor.front and abs(self.left+self.right) > 0) \
                    or (not self.captor.back and abs(self.left+self.right) < 0)):
                self.state = u"run"
                self.can.send(u"asserv speed %d %d" %(self.left, self.right))
                self.missions[u"threshold"].sensivity(abs(self.left+self.right) / 100)
                
    def process_event(self, event):
        if event.name == u"captor":
            if self.state != u"repos":
                if ((event.pos == u"front" and abs(self.left+self.right) > 0) \
                        or (event.pos == u"back" and abs(self.left+self.right) < 0)):
                    if event.state == u"start":
                        self.resume()
                    else:
                        self.pause()

        elif event.name == u"asserv" and event.type == u"done":
            if self.state == u"pausing":
                self.state = u"paused"
                self.resume()
            elif self.state == u"stopping":
                self.state = u"repos"
                self.missions[u"threshold"].sensivity(1)
                self.send_event(Event(u"speedrotate", u"done", self.callback))
            elif self.state == u"aborting":
                self.state = u"repos"
                self.missions[u"threshold"].sensivity(1)
                self.send_event(Event(u"speedrotate", u"aborted", self.callback))
