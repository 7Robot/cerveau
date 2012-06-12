# -*- coding: utf-8 -*-

from events.event import Event
from events.event import CmdError
from itertools import imap

class TurretEvent(Event):
    def __init__(self, cmd):
        super(self.__class__,self).__init__()
        self.type   = cmd[1]
        self.angle  = []
        self.dist   = []

        if self.type == u"answer":
            if len(cmd) < 11:
                values  = list(imap(self.parse_int,cmd[2:])) 
                for i in xrange(len(values)):
                    if i%2 == 0:
                        self.dist.append(values[i])
                    else:
                        self.angle.append(values[i])
            else:
                raise CmdError(u" turret answer  must be followed by "
                        +u" a maximum of height integers")
        
        elif self.type in [u"request", u"mute", u"unmute", u"on", u"off"]:
            if len(cmd) != 2:
                raise CmdError(u" %s %s  takes no argument"
                         %(cmd[0], cmd[1]))
        else:
            raise CmdError(u" %s  can\'t be followed by  %s "
                    %(cmd[0], cmd[1]))
