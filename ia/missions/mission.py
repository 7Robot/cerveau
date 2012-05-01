# -*-coding:UTF-8 -*

import threading
from events.internal import Timer_end

class Mission:
    def __init__(self, robot):
        ''' Convention state = 0 : état initial (d'attente)'''
        self.state = 0
        self.robot = robot
        name = self.__class__.__name__
        if name[-7:] == "Mission":
            self.name = name[0:-7].lower()
            print("Mission « %s » loaded" %self.name)
        else:
            print("Warning: convention de nommage non respectée pour %s" %name)
            self.name = name.lower()
        
    def process_event(self, event):
        pass

    def create_timer(self, duration):
        '''Créé un timer qui va envoyer un évènement Timer_end à la fin'''
        t = threading.Timer(duration/1000, self.process_event, [Timer_end()])
        t.start()
