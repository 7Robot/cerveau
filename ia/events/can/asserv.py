# -*- coding: utf-8 -*-

from events.event import Event
from events.event import CmdError

class AsservEvent(Event):
    def __init__(self, cmd):
        super(self.__class__,self).__init__()
        self.type = cmd[1]
        
        # asserv dist/rot
        if self.type == u"dist" or self.type == u"rot":
            if len(cmd) == 3:
                self.value = cmd[2]
            else:
                raise CmdError(u" %s %s  takes exactly 1 argument"
                        %(cmd[0], cmd[1]))
                self.value = self.parse_int(self.value)
            
        # Interruption de consigne
        # ex: asserv int dist 586 (10e de mm)
        # ex : asserv int rot 55132 (centidegr)
        elif self.type == u"int":
            if len(cmd) == 4:
                self.type += u"_" + cmd[2]
                self.value = self.parse_int(cmd[3])
            else:
                raise CmdError(u" %s %s  takes exactly 4 argument"
                        %(cmd[0], cmd[1]))
                self.value = self.parse_int(self.value)
            
        
        # asserv speed
        elif self.type == u"speed":
            if len(cmd) == 4 or len(cmd) == 5:
                self.value = [self.parse_int(cmd[2]), self.parse_int(cmd[3])]
                self.curt  = False
                if len(cmd) == 5:
                    if cmd[4] == u"curt":
                        self.curt = True
                    else:
                        raise CmdError(u"expected  curt  or nothing as fifth "
                                + u"argument, got  %s " %cmd[4])
            else:
                raise CmdError(u" %s %s  takes exactly 2 or 3 arguments"
                        %(cmd[0], cmd[1]))

        # asserv ticks
        elif self.type == u"ticks":
            if len(cmd) == 3 and cmd[2] in [u"reset", u"request"]:
                self.cmd = cmd[2]
            elif len(cmd) == 4 and cmd[2] == u"answer":
                self.cmd = u"answer"
                self.value = self.parse_int(cmd[3])
            else:
                raise CmdError(u" asserv ticks  must be followed by "
                        + u" reset ,  request  or  answer <dist> ")
                
        # asserv stop/on/off/done
        elif self.type in [u"stop", u"on", u"off", u"done"]:
            if len(cmd) != 2:
                raise CmdError(u" %s %s  takes no argument"
                         %(cmd[0], cmd[1]))
        else:
            raise CmdError(u" %s  can\'t be followed by  %s "
                    %(cmd[0], cmd[1]))
