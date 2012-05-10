#!/usr/bin/python3
# -*-coding:UTF-8 -*

import logging, logging.config
import socket

from comm.can import Can
from comm.ui  import UI
from dispatcher import Dispatcher

class IA:
    def __init__(self, name, **kargs):
        
        self.logger = logging.getLogger("ia")
        f=open(name+".yml")
        logging.config.dictConfig(yaml.load(f))
        f.close()

        self.logger.info("Starting « %s » robot" % name)
        assert(name in ["petit", "gros"])
        
        module = __import__("robots."+name)
        self.robot = getattr(module, name.capitalize()+"Robot")()
        
        
        # On écrase les attributs du robot par ceux passés ici en argument, utiles pour le testing
        for argument in kargs:
            setattr(self.robot, argument, kargs[argument])
            
                    
        self.can_sock = socket.socket()
        self.ui_sock  = socket.socket()
        
        self.can_sock.connect((robot.can_ip, robot.can_port))
        self.ui_sock.connect((robot.ui_ip, robot.ui_port))
        
        
            
        self.can = Can(self.sock)
        self.ui  = UI(self.sock)
        self.dispatcher = Dispacher(self.robot, self.can, self.ui)
        
        self.can.dispatcher = dispatcher
        self.ui.dispatcher  = ui
        
        self.dispatcher.start() # Mieux si démarre avant can et ui
        self.can.start()
        self.ui.start()

        self.logger.info("IA initialized")
        

if __name__ == "__main__":
    if len(argv) < 1:
        print("Usage: ./ia.py nom_robot")
    else:
        ia = IA(sys.argv[1], **{"ui_ip": "r2d2"})
