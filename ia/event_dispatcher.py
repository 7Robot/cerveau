# -*- coding: utf-8 -*-
import os, threading
from class_manager import *
from events.internal import Start 
from missions.mission import Mission 


class Event_dispatcher:
    '''Dispatch les events et la lance la 1e missions
    du coup faudrait peut être revoir son nom'''
    def __init__(self, missions_prefix):
        # instancier toutes les missions 
        self.missions = {}
        self._load_all_missions(missions_prefix)
        if "StartMission" in self.missions:
            self.missions["StartMission"].process_event(Start())
        else:
            print("startMission not found") #FIXME: utiliser un logger.fatal()
            
        
    def _load_all_missions(self, missions_prefix):
        '''Charge toutes les instances de toutes les missions'''
        assert(missions_prefix in ["petit", "gros"])
        self.missions    = {}
        path             = os.path.dirname(os.path.join(os.getcwd(),"missions", missions_prefix))
        classes_missions = class_loader(path)
        for classe_mission in set(classes_missions):
            if classe_mission.__name__ != "Mission" and issubclass(classe_mission, Mission):
                print ("starting the mission %s" % classe_mission.__name__)
                mission = classe_mission()
                mission.missions = self.missions 
                self.missions[mission.name] = mission      
                
    
    def listener(self, event):
        # Contrairement à notre discussion on devrait pas avoir besoin de verrous
        for missions in self.missions.values():
            missions.process_event(event)
    