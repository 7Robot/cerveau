# -*- coding: utf-8 -*-
'''
Created on 2 mai 2012
'''

from events.event import Event

class PositioningEndEvent(Event):
    def __init__(self, cmd):
        super(self.__class__,self).__init__()
        
