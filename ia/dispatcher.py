# -*- coding: utf-8 -*-

import logging
from queue import Queue
from threading import Thread
import os

from missions.mission import Mission
from tools.class_manager import class_loader 


class Dispatcher(Thread):
    '''Dispatch les events et la lance la mission StartMission'''
    def __init__(self, robot, can, ui):
        Thread.__init__(self)
        self.logger   = logging.getLogger("dispatcher")
        self.robot    = robot
        self.can = can
        self.ui = ui
        # instancier toutes les missions 
        self.missions = {} #TODO : utiliser une classe spcialise qui rattrappe les exceptions "key not found"
        self.queue    = Queue()
        self.logger.info(" Loading all missions ")
        self._load_all_missions(robot.name)
        self.logger.info(" All missions loaded ")
            
        
    def _load_all_missions(self, missions_prefix):
        '''Crr et charge les instances de toutes les missions du package
        missions.missions_prefix'''
        path             = os.path.join(os.getcwd(),"missions", missions_prefix)
        classes_missions = class_loader(path)
        for classe_mission in set(classes_missions):
            if classe_mission.__name__ != "Mission" and issubclass(classe_mission, Mission):
                mission = classe_mission(self.robot, self.can, self.ui)
                mission.missions = self.missions
                mission.dispatch = self 
                self.missions[mission.name] = mission    
                
    
    def add_event(self, event):
        '''Inutile, sauf si on change d'implmentation'''
        self.queue.put(event, True, None) # block=True, timeout=None
    
    def run(self):
        if "move" in self.missions:
            for mission in self.missions:
                self.missions[mission].move = self.missions["move"]
        else:
            self.logger.critical("MoveMission not found")

        if "odo" in self.missions:
            for mission in self.missions:
                self.missions[mission].odo = self.missions["odo"]
        else:
            self.logger.critical("OdoMission not found")

        if "captor" in self.missions:
            for mission in self.missions:
                self.missions[mission].captor = self.missions["captor"]
        else:
            self.logger.critical("CaptorMission not found")

        if "start" in self.missions:
            self.missions["start"].start()
        else:
            self.logger.critical("StartMission not found")
        
        while True:
            event = self.queue.get(True, None) # block=True, timeout=None
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
