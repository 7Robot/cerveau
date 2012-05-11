# -*-coding:UTF-8 -*

import logging
import threading
from events.internal import TimerEvent

class Mission:
    def __init__(self, robot, can, ui):
        ''' Convention state = 0 : état initial (d'attente)'''       
        self.state = 0
        self.robot = robot
        self.can = can
        self.ui = ui
        name = self.__class__.__name__
        self.logger = logging.getLogger("mission."+name)
        if name[-7:] == "Mission":
            self.name = name[0:-7].lower()
            self.logger.info("Mission « %s » loaded" %self.name)
        else:
            self.logger.warning("Warning: convention de nommage non respectée pour %s" %name)
            self.name = name.lower()
        
    def process_event(self, event):
        pass

    def disable(self):
        self.state = 0

    def create_timer(self, duration):
        '''Créé un timer qui va envoyer un évènement Timer_end à la fin'''
        t = threading.Timer(duration/1000, self.process_event, [TimerEvent()]) #TODO: vérifier que le thread se termine bien après le process_event
        t.start()