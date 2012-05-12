# -*- coding: utf-8 -*-
''' Le module pour tous les évènements internes'''

from events.event import Event

class StartEvent(Event):
    '''
    qui lance les machines à étât (missions)
    '''
    def __init__(self):
        super(self.__class__,self).__init__()
        
class TimerEvent(Event):
    '''
    Event interne, survient en fin d'éxecution d'un Timer
    '''
    def __init__(self, dests=[]):
        super(self.__class__,self).__init__(dests)

class MoveEvent(Event):
    def __init__(self, type, dests=[]):
        super(self.__class__,self).__init__(dests)
        self.type = type

class OdoEvent(Event):
    def __init__(self, type, dests=[]):
        super(self.__class__,self).__init__(dests)
        self.type = type


