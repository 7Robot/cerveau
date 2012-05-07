# -*- coding: utf-8 -*-

from events.event import Event
from events.event import CmdError

class TurretEvent(Event):
    def __init__(self, cmd):
        super(self.__class__,self).__init__()
        self.type = cmd[1]

        if self.type == "answer":
            if len(cmd) < 7:
                try:
                    self.value = list(map(int,cmd[2:]))
                except ValueError as e:
                    raise CmdError(e.__str__())
            else:
                raise CmdError("« turret answer » must be followed by "
                        +" a maximum of four integers")
        
        elif self.type in ["request", "mute", "unmute", "on", "off"]:
            if len(cmd) != 2:
                raise CmdError("« %s %s » takes no argument"
                         %(cmd[0], cmd[1]))
        else:
            raise CmdError("« %s » can't be followed by « %s »"
                    %(cmd[0], cmd[1]))
