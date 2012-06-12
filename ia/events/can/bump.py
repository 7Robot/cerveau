# -*- coding: utf-8 -*-

from events.event import Event
from events.event import CmdError

class BumpEvent(Event):
    def __init__(self, cmd):
        super(self.__class__,self).__init__()
        if len(cmd) == 3:
            self.pos = cmd[1].lower()
            self.state = cmd[2]
            if self.state not in [ u"open", u"close" ]:
                raise CmdError(u" bump  must be followed by an id, then "
                        + u" open  or  close ")
        else:
            raise CmdError(u" bump  must be followed by an id, then "
                   + u" open  or  close ")
