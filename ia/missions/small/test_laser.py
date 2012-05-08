# -*- coding: utf-8 -*-
'''
Created on 8 mai 2012
'''

if False:
    
    from math import cos, sin
    
    from missions.mission import Mission
    class TestLaserMission: #(Mission):
        def __init__(self, robot):
            super(self.__class__,self).__init__(robot)
            self.histeresis = 0 # pour éviter les problèmes de clignotement, 
            # on aggrandit le carré (surtout en largeur) qui détermine si on peut y aller ou pas
            
        def process_event(self, e):
            if e.name == "turret" and e.type == "answer":
                free_way = True
                next_histeresis = 0
                for i in range(len(e.angle)):
                    obs_x = e.dist[i]*cos(e.angle[i])
                    obs_y = e.dist[i]*sin(e.angle[i])
                    print(obs_x, obs_y)
                    # la tourelle laser est à 8cm du bord droit, 15cm du bord gauche, TODO, mettre ces params dans le robot
                    if  obs_x < 8+2*self.histeresis and obs_x > -12-2*self.histeresis \
                    and obs_y < 30+self.histeresis:
                        free_way = False
                        next_histeresis = 1
                        print("gêne")
                        break
                    else:
                        print("ne gêne pas")
                self.histeresis = next_histeresis
                    
                if free_way:
                    print("GO !!!!!!!!")
                else:
                    print("NE PAS AVANCER !!!!")