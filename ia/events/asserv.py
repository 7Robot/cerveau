# -*- coding: utf-8 -*-

from events.event import Event
from events.event import CmdError

class AsservEvent(Event):
    def __init__(self, cmd):
        super(self.__class__,self).__init__()
        self.type = cmd[1]
        
        # asserv dist/rot
        if self.type == "dist" or self.type == "rot":
            if len(cmd) == 3:
                self.value = cmd[2]
            else:
                raise CmdError("« %s %s » takes exactly 1 argument"
                        %(cmd[0], cmd[1]))
                self.value = self.parse_int(self.value)
            
        # Interruption de consigne
        # ex: asserv int dist 586 (10e de mm)
        # ex : asserv int rot 55132 (centidegré)
        elif self.type == "int":
            if len(cmd) == 4:
                self.type += "_" + cmd[2]
                self.value = self.parse_int(cmd[3])
            else:
                raise CmdError("« %s %s » takes exactly 4 argument"
                        %(cmd[0], cmd[1]))
                self.value = self.parse_int(self.value)
            
        
        # asserv speed
        elif self.type == "speed":
            if len(cmd) == 4 or len(cmd) == 5:
                self.value = [self.parse_int(cmd[2]), self.parse_int(cmd[3])]
                self.curt  = False
                if len(cmd) == 5:
                    if cmd[4] == "curt":
                        self.curt = True
                    else:
                        raise CmdError("expected « curt » or nothing as fifth "
                                + "argument, got « %s »" %cmd[4])
            else:
                raise CmdError("« %s %s » takes exactly 2 or 3 arguments"
                        %(cmd[0], cmd[1]))
                
        elif self.type == "pos":
            if len(cmd) == 3:
                    self.value = self.parse_int(cmd[2])
            else:
                raise CmdError("« %s %s » must be followed by « dist » or"
                        + " « rot », then by a integer"
                        %(cmd[0], cmd[1]))
                
        # asserv done
        elif self.type == "done":
            if len(cmd) != 2:
                raise CmdError("« %s %s » doesn't take any argument"
                        %(cmd[0], cmd[1]))
                
        elif self.type in ["stop", "on", "off"]:
            if len(cmd) != 2:
                raise CmdError("« %s %s » takes no argument"
                         %(cmd[0], cmd[1]))
        else:
            raise CmdError("« %s » can't be followed by « %s »"
                    %(cmd[0], cmd[1]))
