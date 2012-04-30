# -*- coding: utf-8 -*-
'''
Created on 28 avr. 2012
'''

from ia import IA
from time import sleep
import random
from tests.ia_test import Server_test1
from tests.server import Server_test 
from simulator.simu import Simu
from robot.small_robot import Small_robot 
from robot.simu_robot import Simu_robot
from scene import Scene
import threading


class Server_test1(Server_test):
    def __init__(self, ip='127.0.0.1', port=7773):
        super(self.__class__, self).__init__(ip, port)
        
    def tests(self):
        self.send_cmd("bump back close")
        self.running.wait(0.4)
        self.send_cmd("odo pos 3000 0 0")
        self.running.wait(0.1)
        self.send_cmd("odo asserv done 3000")
        self.running.wait(0.1)
        self.send_cmd("odo pos 3000 3000 0")
        self.running.wait(0.4)
        self.send_cmd("odo pos 3000 3000 90")
        self.running.wait(0.1)
        self.send_cmd("odo asserv rot 900")
        self.running.wait(0.1)
        self.send_cmd("bump back close")
        self.running.wait(0.4)
        self.send_cmd("odo pos 0 3000 -900")
        self.running.wait(0.1)
        self.send_cmd("odo pos 0 3000 -900")
        self.running.wait(0.3)
        self.stop()

if __name__ == '__main__':
    port = random.randint(7700, 7800)
    print ("Serveur de test sur le port %d" % port)
            
    test_server = Server_test1('127.0.0.1',port)
    test_server.start()
    
    sleep(0.5)
    
    
    robot = Simu_robot(Small_robot())
    simu = Simu(robot, Scene())
    ia = IA(robot, "127.0.0.1", port)
    ia_thread = threading.Thread(None, ia.main, None, (), {})
    ia_thread.start()
    simu.main()
    