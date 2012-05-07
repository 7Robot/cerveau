# -*- coding: utf-8 -*-
'''
Created on 29 avr. 2012
'''

from can import Can
import unittest
from events import *

class Test_can(unittest.TestCase):
    def setUp(self):
        self.can = Can(None, None)
        
    def test_asserv(self):
        self.assertIs(type(self.can.cmd_to_event("asserv done\n")), AsservEvent)
        self.assertIs(type(self.can.cmd_to_event("asserv int rot 2645\n")), AsservEvent)
        self.assertIs(type(self.can.cmd_to_event("asserv int dist 2645\n")), AsservEvent)
    def test_bump(self):
        for pos in ["back", "front"]:
            for state in ["open", "close"]:
                self.assertIs(type(self.can.cmd_to_event("bump %s %s\n" % (pos, state))), BumpEvent)
    def test_odo(self):
        self.assertIs(type(self.can.cmd_to_event("odo pos 5 7 65\n")), OdoEvent) 
    def test_sonar(self):
        self.assertIs(type(self.can.cmd_to_event("rangefinder 1 value 15 under edge")), RangefinderEvent)
        self.assertIs(type(self.can.cmd_to_event("rangefinder 1 value 15 over")), RangefinderEvent)
    
if __name__ == '__main__':
    unittest.main()