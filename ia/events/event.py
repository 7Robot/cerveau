# -*- coding: utf-8 -*-

import logging

class Event:
    '''Tous les events fils doivent appeller le constructeur de Event 
    pour initialiser leur attribut "name"'''
    def __init__(self, name = None, type = None, dests=[], **kargs):
        '''En thorie cmd_to_event nous passe une commande avec 2 ou plus arguments'''
        self.logger = logging.getLogger("event")
        if not isinstance(dests,list):
            dests = [dests]
        self.dests   = dests
        '''Raccourci de nommage pour rcuprer le type d'un event'''
        if name == None:
            name = self.__class__.__name__
            if name[-5:] == "Event":
                self.name = name[:-5].lower()
            else:
                self.logger.warning("Warning: convention de nommage non respecte pour %s" %name)
                self.name = name.lower()
        else:
            self.name = name
        self.type = type
        for arg in kargs:
            setattr(self, arg, kargs[arg])

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
