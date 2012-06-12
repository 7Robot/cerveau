#!/usr/bin/python3
# -*-coding: ascii -*

from logging import getLogger
from logging.config import fileConfig
import socket
import sys

from comm.can import Can
from comm.intercom import InterCom
from comm.ui  import UI
from dispatcher import Dispatcher
from robots.robot import Robot
from io import open


class IA(object):
    def __init__(self, name, **kargs):
        
        # Initialisation du logger
        self.logger = getLogger(u"ia")
        f=open(name+u".ini")
        fileConfig(f)
        f.close()

        self.logger.info(u"Starting  %s  robot" % name)
        assert(name in [u"petit", u"gros"])
        
        module = __import__(u"robots."+name)
        self.robot = getattr(getattr(module, name), name.capitalize()+u"Robot")()
        
        Robot.copy_from(self.robot)
        
        # On crase les attributs du robot par ceux passs ici en argument, utiles pour le testing
        for argument in kargs:
            setattr(self.robot, argument, kargs[argument])
            
                    
        self.can_sock = socket.socket()
        self.ui_sock  = socket.socket()
        self.inter  = socket.socket()
        
        self.logger.debug(u"Trying to connect to the CAN")
        self.can_sock.connect((self.robot.can_ip, self.robot.can_port))
        self.logger.debug(u"Trying to connect to the UI")
        self.ui_sock.connect((self.robot.ui_ip, self.robot.ui_port))
        self.logger.debug(u"Trying to connect to the INTERCOMM")
        self.inter.connect((self.robot.inter_ip, self.robot.inter_port))
        
        self.can = Can(self.can_sock)
        self.ui  = UI(self.ui_sock)
        self.inter = InterCom(self.inter)
        self.dispatcher = Dispatcher(self.robot, self.can, self.ui)
        
        self.can.dispatcher = self.dispatcher
        self.ui.dispatcher  = self.dispatcher
        self.inter.dispatcher  = self.dispatcher
        
        self.dispatcher.start() # Mieux si demarre avant can et ui
        self.can.start()
        self.ui.start()
        self.inter.start()

        self.logger.info(u"IA initialized")
        
        self.ui.join()
        
        self.logger.info(u"IA stopped")

if __name__ == u"__main__":
    
    default = u"petit"
    
    if len(sys.argv) < 2:
        print u"Usage: %s <nom_robot>" %sys.argv[0]
        print u"Run default robot '%s'" %default
    else:
        default = sys.argv[1]
    
    ia = IA(default)
