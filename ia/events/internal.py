# -*- coding: utf-8 -*-
''' Le module pour tous les vnements internes'''

from events.event import Event

class CaptorEvent(Event):
    def __init__(self, pos, state, dests=[]):
        super(self.__class__,self).__init__(dests)
        self.pos = pos
        self.state = state


