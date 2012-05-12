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
    def __init__(self):
        super(self.__class__,self).__init__()

class MoveEvent(Event):
    def __init__(self, type):
        super(self.__class__,self).__init__()
        self.type = type

class OdoEvent(Event):
    def __init__(self, type):
        super(self.__class__,self).__init__()
        self.type = type


class RoutingEvent(Event):
    '''Permet d'effectuer du routage d'event
    Si le dispatcher voit un event RoutingEvent, il transmet l'event
    RoutingEvent.event à la mission RoutingEvent.mission'''
    def __init__(self, event, mission):
        super(self.__class__,self).__init__()
        self.event   = event
        self.mission = mission # doit être une instance de TrucMission
