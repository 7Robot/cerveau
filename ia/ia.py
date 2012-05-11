#!/usr/bin/python3
# -*-coding:UTF-8 -*

from logging import getLogger
from logging.config import fileConfig
import socket
import sys

from comm.can import Can
from comm.ui  import UI
from dispatcher import Dispatcher


class IA:
    def __init__(self, name, **kargs):
        
        # Initialisation du logger
        self.logger = getLogger("ia")
        f=open(name+".ini")
        fileConfig(f)
        f.close()

        self.logger.info("Starting « %s » robot" % name)
        assert(name in ["petit", "gros"])
        
        module = __import__("robots."+name)
        self.robot = getattr(getattr(module, name), name.capitalize()+"Robot")()
        
        
        # On écrase les attributs du robot par ceux passés ici en argument, utiles pour le testing
        for argument in kargs:
            setattr(self.robot, argument, kargs[argument])
            
                    
        self.can_sock = socket.socket()
        self.ui_sock  = socket.socket()
        
        self.can_sock.connect((self.robot.can_ip, self.robot.can_port))
        self.ui_sock.connect((self.robot.ui_ip, self.robot.ui_port))
        
        
        self.can = Can(self.can_sock)
        self.ui  = UI(self.ui_sock)
        self.dispatcher = Dispatcher(self.robot, self.can, self.ui)
        
        self.can.dispatcher = self.dispatcher
        self.ui.dispatcher  = self.dispatcher
        
        self.dispatcher.start() # Mieux si démarré avant can et ui
        self.can.start()
        self.ui.start()

        self.logger.info("IA initialized")

if __name__ == "__main__":
    
    default = "petit"
    
    if len(sys.argv) < 2:
        print("Usage: %s nom_robot" %sys.argv[0])
        print("Run default robot « %s » …", default)
    else:
        default = sys.argv[1]
    
    ia = IA(default, **{"ui_ip": "localhost", "can_ip": "localhost",
        "inter_ip": "localhost"})
