# -*- coding: utf-8 -*-
'''
Created on 28 avr. 2012
'''

from ia import IA
from time import sleep
import random
from tests.server import Server_test
from tests.ia_test import Server_test_robot
from simulator.simu import Simu
from robot.small_robot import Small_robot 
from robot.proxy_robot import Proxy_robot
from scene import Scene
import threading

if __name__ == '__main__':
    
    robot = Proxy_robot(Small_robot())
    simu = Simu(robot, Scene())
    ia = IA(robot, "r2d2", 7773, "r2d2", 7775)
    ia_thread = threading.Thread(None, ia.main, None, (), {})
    ia_thread.start()
    simu.main()
    
