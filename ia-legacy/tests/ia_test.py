# -*- coding: utf-8 -*-
'''
Created on 28 avr. 2012
'''

from ia import IA
from robot.small_robot import Small_robot 
from tests.server import Server_test 
from time import sleep
import random

class Server_test_can(Server_test):
    def __init__(self, ip='127.0.0.1', port=7773):
        super(self.__class__, self).__init__(ip, port)
        
    def tests(self):
        
        self.send_cmd("bump back close")
        self.running.wait(0.1)
        self.send_cmd("odo pos 3000 0 0")
        self.running.wait(0.3)
        self.send_cmd("bump back close")
        self.running.wait(0.1)
        self.send_cmd("odo pos 0 3000 -900")
        self.running.wait(0.1)
        self.stop()

class Server_test_robot(Server_test):
    def __init__(self, ip='127.0.0.1', port=7773):
        super(self.__class__, self).__init__(ip, port)
        
    def tests(self):
#        pass
        self.stop()
        
if __name__ == '__main__':
    
    port = random.randint(7700, 8700)
    print ("Serveur de test sur le port %d" % port)
    #a=input("")
            
    test_server_can = Server_test_can('127.0.0.1',port)
    test_server_can.start()
    
    test_server_robot = Server_test_can('127.0.0.1',port+1)
    test_server_robot.start()
    
    sleep(0.3)
    # "127.0.0.1", port, "127.0.0.1", port+1
    ia        = IA(Small_robot())
    ia.main()
    
