# -*- coding: utf-8 -*-
'''
Created on 6 mai 2012
'''

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
        self.running.wait(1)
        values = []
        for i in range(20):
            val = random.randint(20,2300)
            values.append(val)
            self.send_cmd("rangefinder 1 value %d under edge" % val)
            self.send_cmd("rangefinder 2 value %d under edge" % val)
            self.running.wait(0.05)
        
        self.running.wait(1.5)
        mean = sum(values[:16])/len(values[:16])
        print("------------------------------------------")
        print("Expected result:")
        print("answer rangefinder_calibrate 1 done, value is %d" % mean)
        print("------------------------------------------")
        self.stop()

class Server_test_ui(Server_test):
    def __init__(self, ip='127.0.0.1', port=7769):
        super(self.__class__, self).__init__(ip, port)
        
    def tests(self):
        self.send_cmd("rangefinder_calibrate 1")
        self.running.wait(1.5)
        self.stop()
        
if __name__ == '__main__':
    
    port = random.randint(7700, 8700)
    print ("Serveur de test sur le port %d" % port)
    #a=input("")
            
    test_server_can = Server_test_can('127.0.0.1',port)
    test_server_can.start()
    
    test_server_ui = Server_test_ui('127.0.0.1',port+1)
    test_server_ui.start()
    
    sleep(0.3)
    ia        = IA(Small_robot(), "127.0.0.1", port, '127.0.0.1', 1, "127.0.0.1", port+1)
    ia.main()
    
