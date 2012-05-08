# -*- coding: utf-8 -*-
'''
Created on 8 mai 2012
'''

if False:
    
    from math import cos, sin
    from mathutils.type import Vertex
    
    from missions.mission import Mission
    class TestLaserMission: #(Mission):
        def __init__(self, robot):
            super(self.__class__,self).__init__(robot)
            self.obstacles = []
            
        def process_event(self, e):
            if e.name == "turret" and e.type == "answer":
                free_way = True
                for i in range(len(e.angle)):
                    obs_x = e.dist[i]*cos(e.angle[i])
                    obs_y = e.dist[i]*sin(e.angle[i])
                    obstacle = Vertex(obs_x, obs_y)
                    print(obs_x, obs_y)
                    # la tourelle laser est à 8cm du bord droit, 15cm du bord gauche
                    if  obs_x < 8 and obs_x > -12 and obs_y < 30:
                        free_way = False
                        print("gêne")
                        break
                    else:
                        print("ne gêne pas")
                    
                if free_way:
                    print("GO !!!!!!!!")
                else:
                    print("NE PAS AVANCER !!!!")