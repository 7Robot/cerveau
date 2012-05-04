# -*- coding: utf-8 -*-

import logging
from queue import Queue
from threading import Thread, Lock
from logging.handlers import SocketHandler

from class_manager import *
from events.internal import StartEvent
from missions.mission import Mission 


class Event_dispatcher(Thread): # FIXME renommer en Event_Manager
    '''Dispatch les events et la lance la 1e missions
    du coup faudrait peut être revoir son nom'''
    def __init__(self, missions_prefix, robot):
        Thread.__init__(self)
        self.logger = logging.getLogger("Event_dispatcher")
        self.robot = robot
        # instancier toutes les missions 
        self.missions = {}
        self.queue    = Queue()
        self._load_all_missions(missions_prefix)
        self.lock     = Lock()
            
        
    def _load_all_missions(self, missions_prefix):
        '''Charge toutes les instances de toutes les missions'''
        self.missions    = {}
        path             = os.path.join(os.getcwd(),"missions", missions_prefix)
        classes_missions = class_loader(path)
        for classe_mission in set(classes_missions):
            if classe_mission.__name__ != "Mission" and issubclass(classe_mission, Mission):
                mission = classe_mission(self.robot)
                mission.missions = self.missions 
                self.missions[mission.name] = mission      
                
    
    def add_event(self, event):
        '''Inutile, sauf si on change d'implémentation'''
        self.queue.put(event, True, None) # block=True, timeout=None
    
    def run(self):
        if "start" in self.missions:
            self.missions["start"].process_event(StartEvent())
        else:
            self.logger.critical("startMission not found")
        while True:
            event = self.queue.get(True, None) # block=True, timeout=None
            for missions in self.missions.values():
                missions.process_event(event)
