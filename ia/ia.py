#!/usr/bin/python3
# -*-coding:UTF-8 -*

import socket

from can import Can
from robot.small_robot import Small_robot
from event_dispatcher import Event_dispatcher

class IA:
    def __init__(self, robot, ip_can="r2d2", port_can=7773, ip_robot="r2d2", port_robot=7775):
        self.mission_prefix = robot.__class__.__name__.lower().split('_')[0]
        print("Starting « %s » robot" % self.mission_prefix)
        # On ne peut pas avoir "simu" car la class proxy renvoie le __class__.__name__ de l'objet proxié
        assert(self.mission_prefix in ["small", "big", "simu"])
        self.ip         = ip_can
        self.port       = port_can
        self.sock_can   = None
        self.sock_robot = None
        self.sock_can   = self.connect(self.sock_can, ip_can, port_can)
        self.sock_robot = self.connect(self.sock_robot, ip_robot, port_robot)
        
        if self.sock_can != None:
            self.keep_on = False
        else:
            self.keep_on = True
        
        self.robot      = robot
        self.dispatcher = Event_dispatcher(self.mission_prefix, self.robot)
        
        self.msg_can    = Can(self.sock_can, self.dispatcher)
        self.msg_robot  = Can(self.sock_robot, self.dispatcher)
        
        self.robot.msg_can    = self.msg_can
        self.robot.msg_robot  = self.msg_robot
        
        self.dispatcher.start()
        self.msg_can.start()
        self.msg_robot.start()
        print("Robot ready !!!!!!")
        print("msg_can", self.robot.msg_can) 
        
    def connect(self, sock, ip, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, port))
        except socket.error as message:
            if sock:
                sock.shutdown(socket.SHUT_WR) 
                sock.close()
            sock = None # On est sûr de tout arréter 
            # logger.fatal
            print ("Impossible d'otenir une connection : ", message)
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
