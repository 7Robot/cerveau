# -*-coding:UTF-8 -*

import logging
import threading

from events.internal import StartEvent, TimerEvent, RoutingEvent

class Mission:
    def __init__(self, robot, can, ui):
        ''' Convention state = 0 : état initial (d'attente)'''  
        self.dispatch = None      # sera mis a jour par le loader de mission dans dispatcher.py
        self._state = 0
        self.robot = robot
        self.can = can
        self.ui = ui
        name = self.__class__.__name__

        self.logger = logging.getLogger("mission")
        if name[-7:] == "Mission":
            self.name = name[0:-7].lower()
            self.logger.info("Mission « %s » loaded" %self.name)
        else:
            self.logger.warning("Warning: convention de nommage non respectée pour %s" %name)
            self.name = name.lower()
            
        self.logger = logging.getLogger("mission."+self.name)

    def _get_state(self):
        return self._state

    def _set_state(self, state):
        self.logger.info("[%s] %s → %s" %(self.name, self._state, state))
        self._state = state

    state = property(_get_state, _set_state)


    def start(self):
        self.process_event(StartEvent())

    def process_event(self, event):
        pass

    def disable(self):
        self.state = 0

    def create_timer(self, duration):
        '''Créé un timer qui va envoyer un évènement Timer_end à la fin
        self.dispatch.add_event se termine immédiatement après l'ajout dans la queue
        donc le thread du Timer s'arrête après l'execution du add_event()
        donc il n'y a pas de problème d'execution concurrente entre le thread du timer
        et le dispatcher'''
        t = threading.Timer(duration/1000, self.dispatch.add_event, \
                            [RoutingEvent(TimerEvent(), self)])
        t.start()
