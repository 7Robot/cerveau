# -*- coding: utf-8 -*-
'''
Created on 1 mai 2012
'''

# -*- coding: utf-8 -*-
'''
Created on 28 avr. 2012
'''


import random
from time import sleep
import threading

from ia import IA
from mathutils.types import Vertex
from robot.proxy_robot import Proxy_robot
from simulator.simu import Simu
from simulator.simu_robot import Simu_robot, Simu_regulator
from scene import Scene
from tests.ia_test import Server_test1
from tests.server import Server_test


class Server_test1(Server_test):
    def __init__(self, ip='127.0.0.1', port=7773):
        super(self.__class__, self).__init__(ip, port)
        
    def tests(self):
        self.send_cmd("asserv speed -30 -30")
        self.running.wait(2)
        self.send_cmd("asserv dist 3000")
        self.running.wait(1)
        print("rot!!!!!!!!!!")
        self.send_cmd("asserv rot -900")
        self.running.wait(0.5)
        print("rec!!!!!!!!!!")
        self.send_cmd("asserv speed -42 -42")
        self.running.wait(0.7)
        self.send_cmd("asserv dist 3000")
        self.stop()

if __name__ == '__main__':
    port = random.randint(7700, 7800)
    print ("Serveur de test sur le port %d" % port)
            
    test_server = Server_test1('127.0.0.1',port)
    test_server.start()
    
    sleep(0.5)
    
    
    robot = Proxy_robot(Simu_regulator(Simu_robot(Vertex(3000-15000, -3000+10000), 0, 200, 60)))
    
    #robot.regulator.asserv_speed(20, False)
    simu = Simu(robot, Scene())
    ia = IA(robot, "127.0.0.1", port)
    ia_thread = threading.Thread(None, ia.main, None, (), {})
    ia_thread.start()
    simu.main()
    