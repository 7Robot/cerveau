#-*- coding: utf-8 -*-

'''
On charge ici toutes les classes de mission

/ ! \ SI on change le nom de ce module actuellement appelé "missions", 
changer event_dispatcher._load_all_missions() ... 
'''

import os, sys
from class_manager import *
from missions.mission import Mission


path = os.path.dirname(os.path.abspath(__file__))

classes = class_loader(path)
for cls in classes:
    # Ce if est obligtoire car l'introspection donne aussi les classes 
    # importées par les modules de missions
    if issubclass(cls, Mission):
        #print ("cls", cls.__name__)
        setattr(sys.modules[__name__], cls.__name__, cls)
