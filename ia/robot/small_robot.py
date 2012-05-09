# -*- coding: utf-8 -*-
'''
Created on 29 avr. 2012
'''

from robot.robot import Robot

class Small_robot(Robot):
    def __init__(self, ip_can="petit", port_can=7773):
        super(self.__class__, self).__init__(3000-15000, 3000-10000, 0, 1290, 1290, 1190, 920, ip_can, port_can)