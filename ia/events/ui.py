# -*- coding: utf-8 -*-
u'''
Created on 5 mai 2012
'''

from events.event import Event
from events.event import CmdError


class UIEvent(Event):
    def __init__(self, cmd):
        # prcondition : len(cmd) >= 2
        super(self.__class__,self).__init__()
        self.type = cmd[0]
        if self.type == u"calibrate":
            if len(cmd) >= 2:
                # rangefinder_calibrate <id>
                self.id = self.parse_int(cmd[1])
            else:
                raise CmdError(u" %s  takes 2 arguments" %(cmd[0]))
            
        elif self.type == u"get":
            # get <mission> <attribut>
            if len(cmd) == 3:
                self.mission   = cmd[1]
                self.attribute = cmd[2]  
            else:
                raise CmdError(u" %s  takes 3 arguments"
                 %(cmd[0]))
                
        elif self.type == u"init":
            # init <violet|red>
            if len(cmd) == 2:
                self.side = cmd[1]
                if self.side not in [u"red", u"violet"]:
                    raise CmdError(u"Unknown side  %s ." %(cmd[1]))
            else:
                raise CmdError(u" %s  takes 2 arguments" %(cmd[0])) 
                
        elif self.type == u"message":
            # message <message:string>
            self.message = u" ".join(cmd[1:])
                
        elif self.type == u"set":
            # set <mission> <attribut> <type> <value>
            if len(cmd) == 5:
                self.mission   = cmd[1]
                self.attribute = cmd[2]
                self.set_type      = cmd[3]
                self.value     = cmd[4]
                if self.set_type not in [u"str", u"float", u"int"]:
                    raise CmdError(u"Unknown type  %s " %(self.set_type))
                
                # On change le type de la valeur  setter
                if self.set_type == u"int":
                    self.value = int(self.value)
                elif  self.set_type == u"float":
                    self.value = float(self.value)
            else:
                raise CmdError(u" %s  takes 4 arguments"
                 %(cmd[0]))
        
                
        elif self.type == u"test":
            if len(cmd) == 2:
                self.test = cmd[1]
            
        elif self.type not in [u"positioning", u"end"]:
            raise CmdError(u" Unknown command %s" %cmd)
            
          
