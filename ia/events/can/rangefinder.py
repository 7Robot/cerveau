# -*- coding: utf-8 -*-

from events.event import Event
from events.event import CmdError
from robots.robot import Robot

class RangefinderEvent(Event):
    def __init__(self, cmd):
        super(self.__class__,self).__init__()
        

        self.id  = self.parse_int(cmd[1])
        # On inverse les ordres si on dmarrage en position rouge
        if Robot.side == u"red":
            if self.id == 1:
                self.id = 2
            elif self.id == 2:
                self.id = 1
        
        if len(cmd) >= 3:
            # rangefinder <id:int> mute
            # rangefinder <id:int> unmute
            self.type = cmd[2]
            
            types = [u"mute", u"unmute", u"value", u"threshold", u"request"]
            if self.type not in types:
                raise CmdError(u" %s  third argument must be in list "%cmd[0] + types.__str__())
            
            # rangefinder <id:int> threshold <valeur:int>
            if self.type == u"threshold":

                self.value = self.parse_int(cmd[3])
                
            # rangefinder <id:int> value <valeur:int> under|over [edge]
            elif self.type == u"value":
                self.value = self.parse_int(cmd[3])
                self.pos   = cmd[4]
                self.edge  = False
                pos        = [ u"under", u"over" ]
                if len(cmd) == 6 and cmd[5] == u"edge":
                    self.edge = True
                    
                if self.pos not in pos:
                    raise CmdError(u" %s  second argument must be in list "%cmd[0] + pos.__str__())

        else:
            raise CmdError(u" %s  takes exactly 3 or more arguments"%(cmd[0]))
