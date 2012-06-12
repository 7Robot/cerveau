# -*- coding: utf-8 -*-

import logging
from Queue import Queue
from threading import Thread
import os

from missions.mission import Mission
from tools.class_manager import class_loader 


class Dispatcher(Thread):
    u'''Dispatch les events et la lance la mission StartMission'''
    def __init__(self, robot, can, ui):
        Thread.__init__(self)
        self.logger   = logging.getLogger(u"dispatcher")
        self.robot    = robot
        self.can = can
        self.ui = ui
        # instancier toutes les missions 
        self.missions = {} #TODO : utiliser une classe spcialise qui rattrappe les exceptions "key not found"
        self.Queue    = Queue()
        self.logger.info(u" Loading all missions ")
        self._load_all_missions(robot.name)
        self.logger.info(u" All missions loaded ")
            
        
    def _load_all_missions(self, missions_prefix):
        u'''Crr et charge les instances de toutes les missions du package
        missions.missions_prefix'''
        path             = os.path.join(os.getcwdu(),u"missions", missions_prefix)
        classes_missions = class_loader(path)
        for classe_mission in set(classes_missions):
            if classe_mission.__name__ != u"Mission" and issubclass(classe_mission, Mission):
                mission = classe_mission(self.robot, self.can, self.ui)
                mission.missions = self.missions
                mission.dispatch = self 
                self.missions[mission.name] = mission    
                
    
    def add_event(self, event):
        u'''Inutile, sauf si on change d'implmentation'''
        self.Queue.put(event, True, None) # block=True, timeout=None
    
    def run(self):
        if u"move" in self.missions:
            for mission in self.missions:
                self.missions[mission].move = self.missions[u"move"]
        else:
            self.logger.critical(u"MoveMission not found")

        if u"odo" in self.missions:
            for mission in self.missions:
                self.missions[mission].odo = self.missions[u"odo"]
        else:
            self.logger.critical(u"OdoMission not found")

        if u"captor" in self.missions:
            for mission in self.missions:
                self.missions[mission].captor = self.missions[u"captor"]
        else:
            self.logger.critical(u"CaptorMission not found")

        if u"start" in self.missions:
            self.missions[u"start"].start()
        else:
            self.logger.critical(u"StartMission not found")
        
        while True:
            event = self.Queue.get(True, None) # block=True, timeout=None
            #self.logger.debug("Process event : %s", event.__str__())
            if event.dests != []:
                # Routage de l'event aux destinataires
                for dest in event.dests:
                    dest.process_event(event)
            else:
                # On dispatch l'event  toutes les missions
                for missions in self.missions.values():
                    #self.logger.debug("Send event to %s" %missions.name)
                    missions.process_event(event)
