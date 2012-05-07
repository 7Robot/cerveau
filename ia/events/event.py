# -*- coding: utf-8 -*-

import logging

class Event:
    def __init__(self):
        '''En théorie cmd_to_event nous passe une commande avec 2 ou plus arguments'''
        self.logger = logging.getLogger("event")
        '''Raccourci de nommage pour récupérer le type d'un event'''
        name = self.__class__.__name__
        if name[-5:] == "Event":
            self.name = name[:-5].lower()
        else:
            self.logger.warning("Warning: convention de nommage non respectée pour %s" %name)
            self.name = name.lower()
            
    def parse_int(self, string):
        value = None
        try:
            value = int(string)
        except ValueError as e:
            raise CmdError(e.__str__())
        return value
        
    def __str__(self):
        s = ""
        for i in self.__dict__:
            s += "\t%s:\t%s"%(i, self.__dict__[i].__str__())
        return s

class CmdError(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message
