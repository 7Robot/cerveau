# -*- coding: utf-8 -*-
'''
Created on 9 mai 2012
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
        self.send_cmd("turret answer 12 45") # on est pas dans le petit carré
        
        self.send_cmd("turret answer 11 45") # on est dans le petit carré
        
        self.send_cmd("turret answer 12 45") # pas dans le petit mais dans le gros
        
        self.send_cmd("turret answer 11 45") # on est dans le petit carré
        
        self.send_cmd("turret answer 100 180") # Go !
        

        self.running.wait(3)
        
        print("------------------------------------------")
        print("Expected result:")
        print("------------------------------------------")
        self.stop()

        
if __name__ == '__main__':
    
    port = random.randint(7700, 8700)
    print ("Serveur de test sur le port %d" % port)

            
    test_server_can = Server_test_can('127.0.0.1',port)
    test_server_can.start()

    
    sleep(0.3)
    ia        = IA(Small_robot("127.0.0.1", port))
    ia.main()