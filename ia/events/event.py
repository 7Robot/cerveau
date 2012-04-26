# -*- coding: utf-8 -*-

class Event:
    def name(self):
        '''Raccourci de nommage pour récupérer le type d'un event'''
        return self.__class__.__name
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
