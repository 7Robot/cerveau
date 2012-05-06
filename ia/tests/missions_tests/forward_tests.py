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
    def __init__(self, ip='127.0.0.1', port=7773):
        super(self.__class__, self).__init__(ip, port)
        
    def tests(self):
        self.running.wait(1)
        self.send_cmd("rangefinder 1 value 15 under edge")
        
        self.send_cmd("asserv int dist 300")
        self.running.wait(0.3)
        self.send_cmd("rangefinder 1 value 15 under edge")
        
        self.send_cmd("rangefinder 1 value 100 over edge")
        
        self.send_cmd("rangefinder 1 value 15 under edge")
        self.send_cmd("asserv int dist 200")
        
        self.send_cmd("rangefinder 1 value 15 over edge")
        
        self.send_cmd("asserv done")
        self.running.wait(1)
        
        print("------------------------------------------")
        print("Expected result:")
        print("asserv dist 1000")
        print("asserv stop")
        print("asserv dist 700")
        print("asserv stop")
        print("asserv dist 500")
        print("------------------------------------------")
        self.stop()

        
if __name__ == '__main__':
    
    port = random.randint(7700, 8700)
    print ("Serveur de test sur le port %d" % port)
    #a=input("")
            
    test_server_can = Server_test_can('127.0.0.1',port)
    test_server_can.start()

    
    sleep(0.3)
    ia        = IA(Small_robot(), "127.0.0.1", port)
    ia.main()
    ia.robot.forward(1000)
    
