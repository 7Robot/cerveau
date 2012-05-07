# -*- coding: utf-8 -*-
'''
Created on 29 avr. 2012
'''

import random
import string
import unittest

from can import Can
from events import *
from events.event import CmdError

class Test_can(unittest.TestCase):
    def setUp(self):
        self.can = Can(None, None)
    
    def test_asserv(self):
        self.assertIs(type(self.can.cmd_to_event("asserv done\n")), AsservEvent)
        self.assertIs(type(self.can.cmd_to_event("asserv int rot 2645\n")), AsservEvent)
        self.assertIs(type(self.can.cmd_to_event("asserv int dist 2645\n")), AsservEvent)
    def test_ax(self):
        self.assertIs(type(self.can.cmd_to_event("ax 1 answer 5\n")), AxEvent)
        self.assertIs(type(self.can.cmd_to_event("ax 1 set 5\n")), AxEvent)
    def test_battery(self):
        self.assertIs(type(self.can.cmd_to_event("battery request\n")), BatteryEvent)
        self.assertIs(type(self.can.cmd_to_event("battery answer  11.3\n")), BatteryEvent)
      
    def test_bump(self):
        for pos in ["back", "front"]:
            for state in ["open", "close"]:
                self.assertIs(type(self.can.cmd_to_event("bump %s %s\n" % (pos, state))), BumpEvent)
    def test_fuzzer(self):
        cmds = ["asserv", "ax", "battery", "bump", "odo", "rangefinder", "turret", 
                "done", "int", "rot", "dist", "answer", "request", "value", "under", 
                "over", "back", "front", "edge", "open", "closed", "mute", "unmute", 
                "threshold", "on", "off"]
        for j in range(30):
            cmd = ""
            for i in range(random.randint(1,8)):
                if random.randint(0,2):
                    cmd += cmds[random.randint(0,len(cmds))]
                else:
                    cmd += ''.join(random.choice(string.digits) for x in range(random.randint(1,8)))
                cmd += " "
            print("testing", cmd)
            self.assertRaises(CmdError, self.can.cmd_to_event, cmd)
    def test_odo(self):
        self.assertIs(type(self.can.cmd_to_event("odo pos 5 7 65\n")), OdoEvent) 
    def test_sonar(self):
        self.assertIs(type(self.can.cmd_to_event("rangefinder 1 value 15 under edge")), RangefinderEvent)
        self.assertIs(type(self.can.cmd_to_event("rangefinder 1 value 15 over")), RangefinderEvent)
        self.assertIs(type(self.can.cmd_to_event("rangefinder 2 mute")), RangefinderEvent)
        self.assertIs(type(self.can.cmd_to_event("rangefinder 1 unmute")), RangefinderEvent)
        self.assertIs(type(self.can.cmd_to_event("rangefinder 1 threshold 5000")), RangefinderEvent)
        self.assertIs(type(self.can.cmd_to_event("rangefinder 2 request")), RangefinderEvent)
    def test_turret(self):
        self.assertIs(type(self.can.cmd_to_event("turret answer 1 2 3 4\n")), TurretEvent)
        self.assertIs(type(self.can.cmd_to_event("turret mute\n")), TurretEvent)
        self.assertIs(type(self.can.cmd_to_event("turret unmute\n")), TurretEvent)
        self.assertIs(type(self.can.cmd_to_event("turret on\n")), TurretEvent)
        self.assertIs(type(self.can.cmd_to_event("turret off\n")), TurretEvent)
    
if __name__ == '__main__':
    unittest.main()