# -*- coding: utf-8 -*-
'''
Created on 5 mai 2012
'''

from events.event import Event
from events.event import CmdError

class AxEvent(Event):
    def __init__(self, cmd):
        super(self.__class__,self).__init__()
        self.id = cmd[1]
        if len(cmd) < 3:
            raise CmdError("%s takes 3 or 4 arguments" % cmd[0])
        else:
            # ax 1 request
            self.type = cmd[2]
            
            # ax 1 answer 22
            # ax 1 set 45 (-90 à 90)
            if self.type == "answer" or self.type == "set":
                try:
                    self.value = int(cmd[3])
                except ValueError as e:
                    raise CmdError(e.__str__())