# -*- coding: utf-8 -*-

from events.event import Event
from events.event import CmdError

class BatteryEvent(Event):
    def __init__(self, cmd):
        super(self.__class__,self).__init__()
        self.type = cmd[1]
        if self.type == "answer":
            if len(cmd) == 3:
                try:
                    self.value = float(cmd[2])
                except ValueError as e:
                    raise CmdError(e.__str__())
            else:
                raise CmdError("« %s %s » takes a float argument")
        elif len(cmd) != 2:
            raise CmdError("« %s %s » takes no argument"
                %(cmd[0], cmd[1]))
