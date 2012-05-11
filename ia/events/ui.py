# -*- coding: utf-8 -*-
'''
Created on 5 mai 2012
'''

from events.event import Event
from events.event import CmdError
from mathutils.types import Vertex

class UIEvent(Event):
    def __init__(self, cmd):
        # précondition : len(cmd) >= 2
        super(self.__class__,self).__init__()
        self.type = cmd[0]
        if self.type == "calibrate":
            # rangefinder_calibrate <id>
            self.id = self.parse_int(cmd[1])
            
        elif self.type == "get":
            # get <mission> <attribut>
            if len(cmd) == 3:
                self.mission   = cmd[1]
                self.attribute = cmd[2]  
            else:
                raise CmdError("« %s » takes 3 arguments"
                 %(cmd[0]))
                
        elif self.type == "set":
            # set <mission> <attribut> <type> <value>
            if len(cmd) == 5:
                self.mission   = cmd[1]
                self.attribute = cmd[2]
                self.set_type      = cmd[3]
                self.value     = cmd[4]
                if self.set_type not in ["str", "float", "int"]:
                    raise CmdError("Unknown type « %s »" %(self.set_type))
                
                # On change le type de la valeur à setter
                if self.set_type == "int":
                    self.value = int(self.value)
                elif  self.set_type == "float":
                    self.value = float(self.value)
            else:
                raise CmdError("« %s » takes 4 arguments"
                 %(cmd[0]))
                
        elif self.type == "test":
            self.test = cmd[1]
            
        else:
            raise CmdError("« Unknown command %s %s"
                        %(cmd[0], cmd[1]))
            
            