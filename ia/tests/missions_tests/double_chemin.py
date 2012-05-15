# -*- coding: utf-8 -*-
'''
Created on 15 mai 2012
'''
# -*- coding: utf-8 -*-
'''
Created on 6 mai 2012
'''


from ia import IA
from tests.server_test import Server_test 
from time import sleep
import random

class Server_test_ui(Server_test):
    def __init__(self, ip='127.0.0.1', port=7774):
        super(self.__class__, self).__init__(ip, port)
        
    def tests(self):
        self.running.wait(0.8)
        self.send_cmd("test forward")
        self.running.wait(3)
        self.stop()

class Server_test_can(Server_test):
    def __init__(self, ip='127.0.0.1', port=7773):
        super(self.__class__, self).__init__(ip, port)
        
    def tests(self):
        self.running.wait(2)
        self.send_cmd("rangefinder 1 value 15 under edge")
        
        self.send_cmd("asserv int dist 300")
        self.running.wait(0.3)
        self.send_cmd("rangefinder 1 value 15 under edge")
        self.send_cmd("asserv int dist 300")
        
        self.send_cmd("asserv done")
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
    
    test_server_ui = Server_test_ui('127.0.0.1',port+1)
    test_server_ui.start()

    
    sleep(0.1)
    ia        = IA("petit", **{"can_ip" : "localhost", "can_port" : port, \
                                "ui_ip": "localhost", "ui_port" : port+1})
