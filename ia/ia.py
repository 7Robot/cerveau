#!/usr/bin/python3
# -*-coding:UTF-8 -*

import logging, logging.config 
from logging.handlers import SocketHandler
import socket
import yaml

from can import Can, Wifi, UI
from robot.small_robot import Small_robot
from event_dispatcher import Event_dispatcher

class IA:
    def __init__(self, robot, ip_can="localhost", port_can=7773, ip_robot="r2d2", port_robot=7780, ip_ui="localhost", port_ui=7774):
        self.logger = logging.getLogger("ia")
        self.mission_prefix = robot.__class__.__name__.lower().split('_')[0]
        f=open(self.mission_prefix+".yml")
        logging.config.dictConfig(yaml.load(f))
        f.close()
        
        self.logger.info("Starting « %s » robot" % self.mission_prefix)
        # On ne peut pas avoir "simu" car la class proxy renvoie le __class__.__name__ de l'objet proxié
        assert(self.mission_prefix in ["small", "big", "simu"])
        self.ip         = ip_can
        self.port       = port_can

        self.sock_can   = self.connect(ip_can, port_can)
        self.sock_robot = self.connect(ip_robot, port_robot)
        self.sock_ui    = self.connect(ip_ui, port_ui)
        
        # TODO: faire en sortes que si "self.sock_robot" casser l'ia ne plante pas
        
        if self.sock_can != None:
            self.keep_on = False
            self.logger.critical("IA: Failed to get a socket.")
        else:
            self.keep_on = True
        
        self.robot      = robot
        self.dispatcher = Event_dispatcher(self.mission_prefix, self.robot)
        
        self.msg_can    = Can (self.sock_can, self.dispatcher)
        self.msg_robot  = Wifi(self.sock_robot, self.dispatcher)
        self.msg_ui     =   UI(self.sock_ui, self.dispatcher)
        
        self.robot.msg_can    = self.msg_can
        self.robot.msg_robot  = self.msg_robot
        self.robot.msg_ui     = self.msg_ui
        
        self.dispatcher.start()
        self.msg_can.start()
        self.msg_robot.start()
        self.msg_ui.start()
        self.logger.info("IA initialized")
        
    def connect(self, ip, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, port))
        except socket.error as message:
            if sock: 
                sock.close()
            sock = None # On est sûr de tout arréter 
            self.logger.critical("Impossible d'otenir une connection pour %s %d : %s" % (ip, port, message))
        return sock 
        
        
    def main(self):
        '''Un peu inutile finalement'''
        pass
        
                

    def stop(self):
        self.sock_can.shutdown(socket.SHUT_WR) 
        self.sock_can.close()

if __name__ == "__main__":
    ia = IA(Small_robot())
    ia.main()
#   ev = Event_dispatcher("small", None)
#   ev.start()
