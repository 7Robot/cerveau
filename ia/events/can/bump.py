# -*- coding: utf-8 -*-

from events.event import Event
from events.event import CmdError

class BumpEvent(Event):
    def __init__(self, cmd):
        super(self.__class__,self).__init__()
        if len(cmd) == 3:
            self.pos = cmd[1].lower()
            self.state = cmd[2]
            if self.state not in [ "open", "close" ]:
                raise CmdError(" bump  must be followed by an id, then "
                        + " open  or  close ")
        else:
            raise CmdError(" bump  must be followed by an id, then "
                   + " open  or  close ")
