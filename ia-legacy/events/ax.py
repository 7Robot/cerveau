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
        if len(cmd) < 4:
            raise CmdError("%s takes 4 or 5 arguments" % cmd[0])
        else:
            self.type = cmd[2]
            self.cmd = cmd[3]
           
            # ax 1 angle request
            # ax 1 angle answer 22
            # ax 1 angle set 45 (-90 à 90)
            if self.type == "answer" or self.type == "set":
                if len(cmd) == 4:
                    self.value = self.parse_int(cmd[3])
                else:
                    raise CmdError("« ax <id> <angle/torque> <answer/set> "
                            +"must be followed by an integer")
