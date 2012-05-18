# -*-coding:UTF-8 -*

import logging
import threading

from events.event import Event

class Mission:
    def __init__(self, robot, can, ui):
        ''' Convention state = 0 : tat initial (d'attente)'''  
        self.dispatch = None      # sera mis a jour par le loader de mission dans dispatcher.py
        self._state = 0
        self.robot = robot
        self.can = can
        self.ui = ui
        name = self.__class__.__name__

        self.logger = logging.getLogger("mission")
        if name[-7:] == "Mission":
            self.name = name[0:-7].lower()
            self.logger.info("Mission '%s' loaded" %self.name)
        else:
            self.logger.warning("Warning: convention de nommage non respecte pour %s" %name)
            self.name = name.lower()
            
        self.logger = logging.getLogger("mission."+self.name)

    def _get_state(self):
        return self._state

    def _set_state(self, state):
        self.logger.info("[state] %s -> %s" %(self._state, state))
        self._state = state

    state = property(_get_state, _set_state)


    def start(self):
        self.process_event(Event("start"))

    def process_event(self, event):
        pass

    def disable(self):
        self.state = 0

    def create_timer(self, duration, name="Timer"):
        '''Cr un timer qui va envoyer un vnement Timer_end  la fin
        self.dispatch.add_event se termine immdiatement aprs l'ajout dans la queue
        donc le thread du Timer s'arrte aprs l'execution du add_event()
        donc il n'y a pas de problme d'execution concurrente entre le thread du timer
        et le dispatcher'''
        t = threading.Timer(duration/1000, self.dispatch.add_event, \
                            [Event("timer", "timeout", self, **{'timername':name})])
        t.start()

    def send_event(self, event):
        self.dispatch.add_event(event)
