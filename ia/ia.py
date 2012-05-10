#!/usr/bin/python3
# -*-coding:UTF-8 -*

import logging, logging.config 
import yaml


from robot.small_robot import Small_robot
from robot.big_robot import Big_robot


class IA:
    def __init__(self, robot):
        self.robot = robot
        self.logger = logging.getLogger("ia")
        f = open("small.yml") #FIXME
        f=open(robot.mission_prefix+".yml")
        logging.config.dictConfig(yaml.load(f))
        f.close()
        
        self.logger.info("Starting « %s » robot" % robot.mission_prefix)
        # On ne peut pas avoir "simu" car la class proxy renvoie le __class__.__name__ de l'objet proxié
        assert(robot.mission_prefix in ["small", "big", "simu"])


        
        
        # TODO: faire en sortes que si "self.sock_robot" casser l'ia ne plante pas
        
#        if self.sock_can == None:
#            self.keep_on = False
#            self.logger.critical("IA: Failed to get a socket.")
#        else:
#            self.keep_on = True
        
        
        
        self.logger.info("IA initialized")
        
     
        
        
    def main(self):
        '''Un peu inutile finalement'''
        pass
        
                

    

if __name__ == "__main__":
    #ia = IA(Small_robot())
    ia = IA(Big_robot())
    ia.main()
#   ev = Event_dispatcher("small", None)
#   ev.start()
