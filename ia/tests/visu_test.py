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


class Server_test1(Server_test):
    def __init__(self, ip='127.0.0.1', port=7773):
        super(self.__class__, self).__init__(ip, port)
        
    def tests(self):
        self.send_cmd("bump back close")
        self.running.wait(0.4)
        self.send_cmd("odo pos -1200 -700 0")
        self.running.wait(0.1)
        self.send_cmd("asserv done")
        self.running.wait(0.1)
        self.send_cmd("odo pos -1500 -700 0")
        self.running.wait(0.4)
        self.send_cmd("asserv done")
        self.running.wait(0.1)
        self.send_cmd("odo pos -1200 -700 -9000")
        self.running.wait(0.1)
        self.send_cmd("bump back close")
        self.running.wait(0.4)
        self.send_cmd("odo pos -1200 -1000 -9000")
        self.stop()

if __name__ == '__main__':
    port = random.randint(7700, 7800)
    print ("Serveur de test sur le port %d" % port)
            
    test_server = Server_test1('127.0.0.1',port)
    test_server.start()
    
    test_server_robot = Server_test_robot('127.0.0.1',port+1)
    test_server_robot.start()
    
    sleep(0.5)
    
    
    robot = Proxy_robot(Small_robot())
    simu = Simu(robot, Scene())
    ia = IA(robot, "127.0.0.1", port,"127.0.0.1", port+1)
    ia_thread = threading.Thread(None, ia.main, None, (), {})
    ia_thread.start()
    simu.main()
    