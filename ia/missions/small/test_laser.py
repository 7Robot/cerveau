# -*- coding: utf-8 -*-
'''
Created on 8 mai 2012
'''

from math import cos, sin, pi

from missions.mission import Mission
class TestLaserMission(Mission): #(Mission):
    def __init__(self, robot):
        super(self.__class__,self).__init__(robot)
        self.histeresis = 0 # pour éviter les problèmes de clignotement, 
        # on aggrandit le carré (surtout en largeur) qui détermine si on peut y aller ou pas
        
    def process_event(self, e):
        if e.name == "turret" and e.type == "answer":
            free_way = True
            next_histeresis = 0
            for i in range(len(e.angle)):
                e.dist[i] -= 8
                obs_x = e.dist[i]*cos(e.angle[i]/180*pi)
                obs_y = e.dist[i]*sin(e.angle[i]/180*pi)
#                print(obs_x, obs_y)
                # la tourelle laser est à 8cm du bord droit, 15cm du bord gauche, TODO, mettre ces params dans le robot
                print("X: %d, Y: %d, histeresis: %d" %(obs_x, obs_y, self.histeresis))
                if  obs_x < 10+8*self.histeresis and obs_x > -12-8*self.histeresis \
                and obs_y < 30+4*self.histeresis:
                    free_way = False
                    histeresis = 1
                    next_histeresis = 1
#                    print("gêne")
                    break
            self.histeresis = next_histeresis
                
            if free_way:
                print("GO !!!!!!!!")
            else:
                print("NE PAS AVANCER !!!!")
