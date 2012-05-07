# -*- coding: utf-8 -*-
'''
Created on 6 mai 2012
'''


from ia import IA
from robot.small_robot import Small_robot 
from tests.server import Server_test 
from time import sleep
import random

class Server_test_can(Server_test):
    def __init__(self, ip='127.0.0.1', port=7773, wifi=True):
        super(self.__class__, self).__init__(ip, port)
        self.wifi = wifi
        
    def tests(self):
        self.running.wait(1)
        self.send_cmd("asserv done")
        
        self.send_cmd("bump back close")
        self.running.wait(1)
        
        self.send_cmd("asserv done")
        
        self.send_cmd("asserv done")
        
        self.send_cmd("bump back close")
        self.running.wait(1)
        
        if self.wifi:
            self.send_cmd("robot gros ready")
        else:
            self.running.wait(23)
            
        self.send_cmd("asserv done")
        

        
        
        print("------------------------------------------")
        print("Expected result:")
        print("INFO - Petit en position !")
        print("------------------------------------------")
        self.stop()

        
if __name__ == '__main__':
    
    port = random.randint(7700, 8700)
    print ("Serveur de test sur le port %d" % port)

            
    test_server_can = Server_test_can('127.0.0.1',port, False) # TODO : faire le test avec True et False
    test_server_can.start()

    
    sleep(0.3)
    ia        = IA(Small_robot(), "127.0.0.1", port)
    ia.main()

    
