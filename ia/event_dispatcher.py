# -*- coding: utf-8 -*-
import os
from os.path import  join
from class_manager import *

class Event_dispatcher:
    def __init__(self):
        # instancier toutes les missions
        self.missions = {}
        self._load_all_missions()
        
    def _load_all_missions(self):
        path = os.path.dirname(join(os.getcwd(),"missions"))
        classes = class_loader(path)       
                
    
    def listener(self, event):
        # Contrairement à notre discussion on devrait pas avoir besoin de verrous
        pass