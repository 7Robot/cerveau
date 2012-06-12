# -*- coding: utf-8 -*-

from events.event import Event
from events.event import CmdError

class BatteryEvent(Event):
    def __init__(self, cmd):
        super(self.__class__,self).__init__()
        self.type = cmd[1]
        if self.type == u"answer":
            if len(cmd) == 3:
                try:
                    self.value = float(cmd[2])
                except ValueError, e:
                    raise CmdError(e.__str__())
            else:
                raise CmdError(u" %s %s  takes a float argument")
        elif len(cmd) != 2:
            raise CmdError(u" %s %s  takes no argument"
                %(cmd[0], cmd[1]))
